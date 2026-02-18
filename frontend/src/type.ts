export type SensorReading = {
  timestamp: string; // ISO 8601 format
  temperature: number; // in Celsius
    humidity: number; // in percentage
}

export type ConnectionStatus = 'connected' | 'open' | 'closed' | 'error';