"""Service layer for sensor data operations."""

import random

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models import SensorData


class SensorDataService:
    """Service class for sensor data operations."""

    @staticmethod
    async def get_latest_sensor_data(
        session: AsyncSession, limit: int = 200
    ) -> list[SensorData]:
        """Fetch the latest sensor data readings from the database.

        Args:
            session: The database session.
            limit: Maximum number of readings to return.

        Returns:
            List of SensorData instances ordered from oldest to newest.
        """
        statement = (
            select(SensorData).order_by(SensorData.timestamp.desc()).limit(limit)
        )

        result = await session.exec(statement)
        readings = list(result.all())

        # Reverse to return oldest to newest
        return list(reversed(readings))

    @staticmethod
    async def generate_sensor_data(session: AsyncSession) -> SensorData:
        """Generate and save sensor data to the database.

        Args:
            session: The database session.

        Returns:
            The created SensorData instance.
        """
        temp = round(random.uniform(18.0, 26.0), 1)
        hum = round(random.uniform(30.0, 65.0), 1)

        sensor_data = SensorData(temperature=temp, humidity=hum)

        session.add(sensor_data)
        await session.commit()
        await session.refresh(sensor_data)

        return sensor_data


# Create a singleton instance for convenience
sensor_service = SensorDataService()
