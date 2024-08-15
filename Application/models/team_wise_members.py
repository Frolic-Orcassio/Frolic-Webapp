from Application import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

class TeamWiseMembers(db.Model): # type: ignore
    team_member_association_id = mapped_column(primary_key=True, autoincrement=True, init=False)
    participant_email: Mapped[str] = mapped_column(ForeignKey('participant.email'), nullable=False, init=False)
    team_id: Mapped[int] = mapped_column(ForeignKey('team.team_id'), nullable=False, init=False)