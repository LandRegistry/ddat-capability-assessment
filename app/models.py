import json
import uuid
from datetime import datetime

from sqlalchemy import UUID, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from app import db


class Role(db.Model):
    # Fields
    id: Mapped[str] = mapped_column(UUID, primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)

    # Methods
    def __init__(self, title):
        self.id = str(uuid.uuid4())
        self.title = title.strip().title()
        self.created_at = datetime.utcnow()

    def __repr__(self):
        return json.dumps(self.as_dict(), separators=(",", ":"))

    def as_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
