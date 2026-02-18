import asyncio
import logging

from fastapi import Depends, FastAPI, Query, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel.ext.asyncio.session import AsyncSession

from app.config import settings
from app.connection_manager import manager
from app.database import get_session, init_db, session_maker
from app.logging import setup_logging
from app.models import SensorData
from app.service import sensor_service

setup_logging()

logger = logging.getLogger("fastapi-realtime-dashboard")

# Background task reference for sensor data production
producer_task: asyncio.Task | None = None


async def sensor_data_producer() -> None:
    """Background task to generate and broadcast sensor data."""
    logger.info("Sensor data producer started.")
    try:
        while True:
            if manager.count > 0:
                # Generate and save sensor data
                async with session_maker() as session:
                    data = await sensor_service.generate_sensor_data(session)

                # Broadcast to all connected clients with proper message format
                await manager.broadcast_json(
                    {"type": "update", "data": data.model_dump(mode="json")}
                )

            await asyncio.sleep(settings.broadcast_interval_seconds)
    except asyncio.CancelledError:
        logger.info("Sensor data producer cancelled.")
    except Exception:
        logger.exception("Sensor data producer error.")
    finally:
        logger.info("Sensor data producer stopped.")


async def lifespan(app: FastAPI):
    """Lifespan function to initialize resources on startup."""
    await init_db()
    yield  # Run the application


app = FastAPI(title="Real-Time Dashboard API", lifespan=lifespan)

allowed_origins = [
    origin.strip() for origin in settings.allowed_origins.split(",") if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok"}


@app.get("/history", response_model=list[SensorData])
async def history(
    limit: int = Query(200, ge=1, le=2000), session: AsyncSession = Depends(get_session)
) -> list[SensorData]:
    """Return the last `limit` readings from the database (oldest→newest)."""
    return await sensor_service.get_latest_sensor_data(session, limit)


@app.websocket(settings.ws_route)
async def websocket_endpoint(
    ws: WebSocket, session: AsyncSession = Depends(get_session)
) -> None:
    """
    WebSocket endpoint that keeps the connection open to receive broadcasts.
    Starts sensor data producer when first client connects.
    """
    global producer_task

    await manager.connect(ws)

    # Start producer if not already running
    if producer_task is None or producer_task.done():
        producer_task = asyncio.create_task(sensor_data_producer())

    try:
        # Send initial snapshot
        snapshot = await sensor_service.get_latest_sensor_data(
            session, settings.default_snapshot_size
        )
        await ws.send_json(
            {
                "type": "snapshot",
                "data": [d.model_dump(mode="json") for d in snapshot],
            }
        )
        logger.info(f"Sent snapshot (n={len(snapshot)}) to client.")

        # Keep connection alive and detect disconnects
        while True:
            await ws.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(ws)
    except Exception:
        logger.exception("WebSocket error")
        await manager.close(ws, code=1011, reason="Internal error")
