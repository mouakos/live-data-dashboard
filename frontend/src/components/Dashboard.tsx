import { useLiveData } from "../lib/useLiveData";
import { LiveChart } from "./LiveChart";
import { StatusBadge } from "./StatusBadge";

export function Dashboard() {
  const { data, status, lastError, reset, url } = useLiveData();

  return (
    <div style={{ display: "grid", gap: "1rem" }}>
      <header
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          gap: "1rem",
        }}
      >
        <div>
          <h1 style={{ margin: 0 }}>Live Sensor Dashboard</h1>
          <p style={{ margin: "0.25rem 0", color: "#666" }}>
            Streaming from <code>{url}</code>
          </p>
        </div>
        <StatusBadge status={status} />
      </header>

      <section>
        <LiveChart data={data} />
      </section>

      <section
        style={{
          display: "flex",
          gap: "0.5rem",
          alignItems: "center",
          justifyContent: "space-between",
          flexWrap: "wrap",
        }}
      >
        <div style={{ display: "flex", gap: "0.5rem" }}>
          <button
            onClick={reset}
            style={{
              padding: "0.5rem 0.75rem",
              borderRadius: "8px",
              border: "1px solid #ddd",
              background: "#f9f9f9",
              cursor: "pointer",
            }}
          >
            Clear Data
          </button>
        </div>
        <div style={{ color: "#a33", minHeight: "1.25rem" }}>
          {lastError ? `Error: ${lastError}` : null}
        </div>
      </section>

      <section
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(240px, 1fr))",
          gap: "0.75rem",
        }}
      >
        <MetricCard label="Latest Temperature (°C)" value={data.at(-1)?.temperature} />
        <MetricCard label="Latest Humidity (%)" value={data.at(-1)?.humidity} />
        <MetricCard label="Samples (last window)" value={data.length} />
      </section>
    </div>
  );
}

function MetricCard({ label, value }: { label: string; value: number | undefined }) {
  return (
    <div
      style={{
        border: "1px solid #eee",
        borderRadius: "12px",
        padding: "0.75rem 1rem",
        boxShadow: "0 1px 0 rgba(0,0,0,0.04)",
        background: "white",
      }}
    >
      <div style={{ fontSize: "0.9rem", color: "#666" }}>{label}</div>
      <div style={{ fontSize: "1.5rem", fontWeight: 600 }}>
        {typeof value === "number" ? value.toFixed(1) : "—"}
      </div>
    </div>
  );
}
