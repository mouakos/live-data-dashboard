import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  Legend,
  ResponsiveContainer,
} from "recharts";
import type { SensorReading } from "../types";

function formatTime(ts: string) {
  try {
    const d = new Date(ts);
    return d.toLocaleTimeString([], { hour12: false });
  } catch {
    return ts;
  }
}

type Props = {
  data: SensorReading[];
};

export function LiveChart({ data }: Props) {
  return (
    <div style={{ width: "100%", height: 360 }}>
      <ResponsiveContainer>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis
            dataKey="timestamp"
            tickFormatter={formatTime}
            minTickGap={24}
          />
          <YAxis yAxisId="left" domain={["auto", "auto"]} />
          <YAxis yAxisId="right" orientation="right" domain={["auto", "auto"]} />
          <Tooltip
            labelFormatter={(label) => `Time: ${formatTime(label as string)}`}
          />
          <Legend />
          <Line
            type="monotone"
            dataKey="temperature"
            yAxisId="left"
            name="Temperature (°C)"
            stroke="#8884d8"
            isAnimationActive={false}
            dot={false}
          />
          <Line
            type="monotone"
            dataKey="humidity"
            yAxisId="right"
            name="Humidity (%)"
            stroke="#82ca9d"
            isAnimationActive={false}
            dot={false}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
