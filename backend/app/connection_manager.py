"""Connection manager for handling WebSocket connections and broadcasting messages to clients."""

import asyncio
import logging
from typing import Any

from fastapi import WebSocket


logger = logging.getLogger("connection_manager")


class ConnectionManager:
    """Manage active WebSocket connections and broadcasting messages."""

    def __init__(self) -> None:
        """Initialize the connection manager."""
        self._connections: set[WebSocket] = set()
        self._lock = asyncio.Lock()

    @property
    def count(self) -> int:
        """Return the current number of active connections."""
        return len(self._connections)

    async def connect(self, ws: WebSocket) -> None:
        """Accept and add a new WebSocket connection to the active set.

        Args:
            ws: The WebSocket connection to add.
        """
        await ws.accept()
        async with self._lock:
            self._connections.add(ws)
            logger.info(f"Client connected. Active={self.count}")

    def disconnect(self, ws: WebSocket) -> None:
        """Remove a WebSocket connection from the active set.

        Args:
            ws: The WebSocket connection to remove.
        """
        self._connections.discard(ws)
        logger.info(f"Client disconnected. Active={self.count}")

    async def broadcast_json(self, payload: dict[str, Any]) -> None:
        """Send JSON payload to all active connections; prune dead ones.

        Args:
            payload: The data to send to clients.
        """
        if not self._connections:
            return
        send_tasks = []
        for ws in list(self._connections):
            send_tasks.append(self._safe_send(ws, payload))
        if send_tasks:
            await asyncio.gather(*send_tasks, return_exceptions=True)

    async def close(
        self, ws: WebSocket, code: int = 1000, reason: str = "normal closure"
    ) -> None:
        """Gracefully close a single socket and remove it.

        Args:
            ws: The WebSocket connection to close.
            code: WebSocket close code (default 1000 for normal closure).
            reason: Optional reason for closure.
        """
        try:
            await ws.close(code=code, reason=reason)
        except Exception:
            pass
        finally:
            self.disconnect(ws)

    async def _safe_send(self, ws: WebSocket, payload: dict[str, Any]) -> None:
        """Send JSON payload to a single WebSocket connection, handling errors.

        Args:
            ws: The WebSocket connection to send data to.
            payload: The data to send.
        """
        try:
            await ws.send_json(payload)
        except Exception as e:
            logger.warning(f"Send failed; removing socket. Error={e}")
            self.disconnect(ws)


manager = ConnectionManager()
