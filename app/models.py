import uuid
from datetime import datetime

import pytz
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
        self.created_at = pytz.utc.localize(datetime.utcnow())
