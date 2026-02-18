import { useEffect, useMemo, useRef, useState } from "react";
import type { ConnectionStatus, SensorReading, ServerMessage } from "../types";

const DEFAULT_WS_URL = "ws://localhost:8000/ws";
const MAX_POINTS = 120;

export function useLiveData(wsUrl?: string, windowSize: number = MAX_POINTS) {
  const url = useMemo(
    () => wsUrl || import.meta.env.VITE_WS_URL || DEFAULT_WS_URL,
    [wsUrl]
  );

  const socketRef = useRef<WebSocket | null>(null);
  const [status, setStatus] = useState<ConnectionStatus>("connecting");
  const [data, setData] = useState<SensorReading[]>([]);
  const [lastError, setLastError] = useState<string | null>(null);
  
  // simple dedupe by timestamp
  const seenRef = useRef<Set<string>>(new Set());

  useEffect(() => {
    const socket = new WebSocket(url);
    socketRef.current = socket;
    setStatus("connecting");
    setLastError(null);

    socket.onopen = () => {
      setStatus("open");
      setLastError(null); // Clear any previous errors
    };

    socket.onmessage = (evt: MessageEvent) => {
      try {
        const msg = JSON.parse(evt.data) as ServerMessage;
        if (msg.type === "snapshot") {
          // Replace data; rebuild dedupe set
          const trimmed = msg.data.slice(-windowSize);
          setData(trimmed);
          seenRef.current = new Set(trimmed.map((r) => r.timestamp));
          setLastError(null); // Clear errors on successful message
          return;
        }
        if (msg.type === "update") {
          const r = msg.data;
          if (seenRef.current.has(r.timestamp)) return; // dedupe
          seenRef.current.add(r.timestamp);
          setData((prev) => {
            const next = [...prev, r];
            if (next.length > windowSize) {
              // also remove from seen set
              const removed = next.length - windowSize;
              for (let i = 0; i < removed; i++) {
                const ts = next[i].timestamp;
                seenRef.current.delete(ts);
              }
              return next.slice(-windowSize);
            }
            return next;
          });
          setLastError(null); // Clear errors on successful message
        }
      } catch (e: unknown) {
        setLastError((e as Error)?.message ?? "Failed to parse message");
      }
    };

    socket.onerror = () => {
      // Only set error if we were previously connected or closed
      // Skip setting error during initial connection attempt
      if (status !== "connecting") {
        setStatus("error");
        setLastError("WebSocket error");
      }
    };

    socket.onclose = () => setStatus("closed");

    return () => {
      socket.close();
      socketRef.current = null;
    };
  }, [url, windowSize]);

  const reset = () => {
    setData([]);
    seenRef.current.clear();
  };

  return { status, data, lastError, reset, url };
}
