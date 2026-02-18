export type SensorReading = {
  timestamp: string; // ISO 8601 format
  temperature: number; // in Celsius
  humidity: number; // in percentage
}

export type SnapshotMessage = { type: "snapshot"; data: SensorReading[] };
export type UpdateMessage   = { type: "update";   data: SensorReading };
export type ServerMessage   = SnapshotMessage | UpdateMessage;

export type ConnectionStatus = 'connecting' | 'open' | 'closed' | 'error';