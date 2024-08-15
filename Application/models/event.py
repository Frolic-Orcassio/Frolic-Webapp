from Application import db, Branch
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from sqlalchemy import String, JSON, ForeignKey
from typing import Optional, List
import datetime

class Event(db.Model): # type: ignore
    event_id: Mapped[Optional[int]] = mapped_column(primary_key=True, autoincrement=True, init=False)

    name: Mapped[str] = mapped_column(String(32), nullable=False, unique=True, init=True)
    branch: Mapped[str] = mapped_column(String(32), nullable=False, init=True)
    # prize: Mapped[Optional[Decimal]] = mapped_column(DECIMAL(10,2), nullable=True, init=True, default=None) 
    description: Mapped[str] = mapped_column(String(512), nullable=False, init=True)
    thumbnail: Mapped[str] = mapped_column(String(64), nullable=False, init=True) # we can add default thumbnail at app configuration and use that value here
    rules: Mapped[JSON] = mapped_column(nullable=False, init=True)
    max_participants: Mapped[Optional[int]] = mapped_column(nullable=True, init=True, default=None)
    allow_registration: Mapped[bool] = mapped_column(nullable=False, init=True, default=True)
    created_at: Mapped[datetime.datetime] = mapped_column(nullable=False, init=False, default=datetime.datetime.now())
    last_modified_at: Mapped[datetime.datetime] = mapped_column(nullable=False, init=False, default=datetime.datetime.now())
    last_modified_by: Mapped[str] = mapped_column(ForeignKey('user.email'), nullable=False, init=True)

    coordinators: Mapped[List["Coordinator"]] = relationship(back_populates='event', init=False, repr=False) # type: ignore
    teams: Mapped[List["Team"]] = relationship(back_populates='event', init=False, repr=False) # type: ignore

    @validates('branch')
    def validate_role(self, key: str, branch: str) -> str:
        if branch not in Branch:
            raise ValueError(f'invalid branch value; Allowed values are: {[r.value for r in Branch]}')
        return branch
    
    @validates('created_at')
    def validate_created_at(self, key: str, value: datetime.datetime) -> datetime.datetime:
        if self.created_at is not None:
            raise ValueError('created_at field is constant')
        return value
    
    @validates('last_modified_at')
    def validate_last_modified_at(self, key: str, value: datetime.date) -> datetime.date:        
        if self.last_modified_at is not None and value < self.last_modified_at:
            raise ValueError("new value for last_modified_at must be greater or equal to old value")
        return value

    @validates('rules')
    def validate_rules(self, key: str, value: dict) -> dict:
        # validate rules with pydantic, the structure should be list of strings
        return value