from Application import db, Role
from sqlalchemy.orm import Mapped, mapped_column, validates, relationship
from sqlalchemy import String, ForeignKey
from typing import Optional, List

class Participant(db.Model): # type: ignore
    email: Mapped[str] = mapped_column(ForeignKey('user.email'), primary_key=True, init=False)

    collage_name: Mapped[str] = mapped_column(String(32), nullable=False, init=True) # we can make StrEnum for this
    branch: Mapped[str] = mapped_column(String(32), nullable=False, init=True)

    user: Mapped["User"] = relationship(back_populates='participant', init=True, repr=True) # type: ignore
    teams: Mapped[List["Team"]] = relationship(back_populates='leader', init=False, repr=False) # type: ignore