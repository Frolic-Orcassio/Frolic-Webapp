from Application import db, Branch
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from sqlalchemy import ForeignKey, String, DECIMAL
from decimal import Decimal
from typing import Optional

class Event(db.Model): # type: ignore
    name: Mapped[str] = mapped_column(String(32), primary_key=True, init=True)
    branch: Mapped[str] = mapped_column(String(32), nullable=False, init=True)
    prize: Mapped[Optional[Decimal]] = mapped_column(DECIMAL(10,2), nullable=True, init=True, default=None) 

    @validates('branch')
    def validate_role(self, key, branch):
        if branch not in Branch:
            raise ValueError(f'invalid branch value; Allowed values are: {[r.value for r in Branch]}')
        return branch