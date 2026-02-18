import { useEffect, useMemo, useRef, useState } from "react";
import type { ConnectionStatus, SensorReading } from "../types";

const DEFAULT_WS_URL = "ws://localhost:8000/ws";
const MAX_POINTS = 120;

export function useLiveData(wsUrl?: string) {
  const url = useMemo(
    () => wsUrl || import.meta.env.VITE_WS_URL || DEFAULT_WS_URL,
    [wsUrl]
  );

  const socketRef = useRef<WebSocket | null>(null);
  const [status, setStatus] = useState<ConnectionStatus>("connecting");
  const [data, setData] = useState<SensorReading[]>([]);
  const [lastError, setLastError] = useState<string | null>(null);

  useEffect(() => {
    const socket = new WebSocket(url);
    socketRef.current = socket;
    setStatus("connecting");
    setLastError(null);

    socket.onopen = () => setStatus("open");

    socket.onmessage = (evt: MessageEvent) => {
      try {
        setLastError(null);
        setStatus("open");
        const reading: SensorReading = JSON.parse(evt.data);
        setData((prev) => {
          const next = [...prev, reading];
          if (next.length > MAX_POINTS) next.shift();
          return next;
        });
      } catch (e: unknown) {
        setLastError((e as Error)?.message ?? "Failed to parse message");
      }
    };

    socket.onerror = () => {
      setStatus("error");
      setLastError("WebSocket error");      
    };

    socket.onclose = () => setStatus("closed");

    return () => {
      socket.close();
      socketRef.current = null;
    };
  }, [url]);

  const reset = () => setData([]);

  return { status, data, lastError, reset, url };
}
