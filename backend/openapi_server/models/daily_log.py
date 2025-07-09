from datetime import date, datetime
from typing import List, Optional
import uuid


class DailyLog:
    """DailyLog model — manually cleaned and updated for SQL schema"""

    def __init__(
            self,
            id: Optional[str] = None,
            title: Optional[str] = None,
            entries: Optional[str] = None,
            log_date: Optional[date] = None,
            tags: Optional[List[str]] = None,
            mood: Optional[str] = None,
            created_at: Optional[datetime] = None,
            updated_at: Optional[datetime] = None,
    ):
        self.id = id or str(uuid.uuid4())
        self.title = title
        self.entries = entries
        self.log_date = log_date
        self.tags = tags or []
        self.mood = mood
        self.created_at = created_at
        self.updated_at = updated_at

    @classmethod
    def from_dict(cls, dikt) -> 'DailyLog':
        """Create DailyLog from dict"""
        return cls(
            id=dikt.get("id"),
            title=dikt.get("title"),
            entries=dikt.get("entries"),
            log_date=dikt.get("log_date"),
            tags=dikt.get("tags", []),
            mood=dikt.get("mood"),
            created_at=dikt.get("created_at"),
            updated_at=dikt.get("updated_at"),
        )

    def to_dict(self) -> dict:
        """Convert DailyLog to dictionary for JSON serialization"""
        return {
            "id": self.id,
            "title": self.title,
            "entries": self.entries,
            "log_date": self.log_date,
            "tags": self.tags,
            "mood": self.mood,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


class UpdateLog:
    """UpdateLog model (for PUT requests) — does NOT include ID or timestamps"""

    def __init__(
            self,
            title: Optional[str] = None,
            entries: Optional[str] = None,
            log_date: Optional[date] = None,
            tags: Optional[List[str]] = None,
            mood: Optional[str] = None,
    ):
        self.title = title
        self.entries = entries
        self.log_date = log_date
        self.tags = tags or []
        self.mood = mood

    @classmethod
    def from_dict(cls, dikt) -> 'UpdateLog':
        return cls(
            title=dikt.get("title"),
            entries=dikt.get("entries"),
            log_date=dikt.get("log_date"),
            tags=dikt.get("tags", []),
            mood=dikt.get("mood"),
        )
