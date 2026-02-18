import type { ConnectionStatus } from "../types";

export function StatusBadge({ status }: { status: ConnectionStatus }) {
  const color =
    status === "open"
      ? "bg-green-600"
      : status === "connecting"
      ? "bg-yellow-600"
      : status === "error"
      ? "bg-red-600"
      : "bg-gray-600";

  return (
    <span
      style={{
        display: "inline-flex",
        alignItems: "center",
        gap: "0.5rem",
        padding: "0.25rem 0.5rem",
        borderRadius: "999px",
        color: "white",
        fontSize: "0.875rem",
      }}
      className={color}
    >
      ● {status.toUpperCase()}
    </span>
  );
}
