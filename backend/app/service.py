"""Service layer for handling reading data operations."""


from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models import Reading


class ReadingService:
    """Service layer for handling reading data operations."""

    @staticmethod
    async def get_latest_reading(
        session: AsyncSession, limit: int = 200
    ) -> list[Reading]:
        """Fetch the latest readings from the database.

        Args:
            session: The database session.
            limit: Maximum number of readings to return.

        Returns:
            List of Reading instances ordered from oldest to newest.
        """
        statement = (
            select(Reading).order_by(Reading.timestamp.desc()).limit(limit)
        )

        result = await session.exec(statement)
        readings = list(result.all())

        # Reverse to return oldest to newest
        return list(reversed(readings))
    
    @staticmethod
    async def create_reading(session: AsyncSession, temperature: float, humidity: float) -> Reading:
        """Create and save a new reading entry to the database.

        Args:
            session: The database session.
            temperature: The temperature reading.
            humidity: The humidity reading.
        Returns:
            The created Reading instance.
        """
        reading = Reading(temperature=temperature, humidity=humidity)

        session.add(reading)
        await session.commit()
        await session.refresh(reading)

        return reading


# Create a singleton instance for convenience
reading_service = ReadingService()
