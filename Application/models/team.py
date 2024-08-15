from Application import db, Role
from sqlalchemy.orm import Mapped, mapped_column, validates, relationship
from sqlalchemy import String, ForeignKey
from typing import Optional

class Team(db.Model): # type: ignore
    team_id: Mapped[Optional[int]] = mapped_column(primary_key=True, autoincrement=True, init=False)
    leader_email: Mapped[str] = mapped_column(ForeignKey('participant.email'), nullable=False, init=False)
    event_id: Mapped[int] = mapped_column(ForeignKey('event.event_id'), nullable=False, init=False)

    leader: Mapped["Participant"] = relationship(back_populates='teams', init=True, repr=True) # type: ignore
    event: Mapped["Event"] = relationship(back_populates='teams', init=True, repr=True) # type: ignore
