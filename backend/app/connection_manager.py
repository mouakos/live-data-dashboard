import asyncio
import logging
from typing import Any

from fastapi import WebSocket


logger = logging.getLogger("connection_manager")


class ConnectionManager:
    def __init__(self) -> None:
        self._connections: set[WebSocket] = set()
        self._lock = asyncio.Lock()

    @property
    def count(self) -> int:
        return len(self._connections)

    async def connect(self, ws: WebSocket) -> None:
        await ws.accept()
        async with self._lock:
            self._connections.add(ws)
            logger.info(f"Client connected. Active={self.count}")

    def disconnect(self, ws: WebSocket) -> None:
        self._connections.discard(ws)
        logger.info(f"Client disconnected. Active={self.count}")

    async def broadcast_json(self, payload: dict[str, Any]) -> None:
        """Send JSON payload to all active connections; prune dead ones."""
        if not self._connections:
            return
        send_tasks = []
        for ws in list(self._connections):
            send_tasks.append(self._safe_send(ws, payload))
        if send_tasks:
            await asyncio.gather(*send_tasks, return_exceptions=True)

    async def _safe_send(self, ws: WebSocket, payload: dict[str, Any]) -> None:
        try:
            await ws.send_json(payload)
        except Exception as e:
            logger.warning(f"Send failed; removing socket. Error={e}")
            self.disconnect(ws)


manager = ConnectionManager()
