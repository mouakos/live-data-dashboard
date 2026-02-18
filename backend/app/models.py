from datetime import datetime, timezone

from sqlmodel import Field, SQLModel


class Reading(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc).astimezone()
    )
    temperature: float
    humidity: float
