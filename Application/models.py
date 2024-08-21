from Application import db, Role, Branch
from sqlalchemy.orm import Mapped, mapped_column, validates, relationship
from sqlalchemy import String, ForeignKey
from typing import Optional, List
import datetime



class User(db.Model): # type: ignore
    email: Mapped[str] = mapped_column(String(320), primary_key=True, init=True)
    is_authenticated: Mapped[bool] = mapped_column(nullable=False, init=True)
    name: Mapped[str] = mapped_column(String(64), nullable=True, init=True, default=None)
    dp: Mapped[Optional[str]] = mapped_column(String(64), nullable=True, init=True, default=None)
    role: Mapped[str] = mapped_column(String(16), nullable=False, init=True, default=Role.PARTICIPANT)

    branch_admin: Mapped[Optional["BranchAdmin"]] = relationship(back_populates='user', uselist=False, init=False, repr=False, cascade="all, delete")
    coordinator: Mapped[Optional["Coordinator"]] = relationship(back_populates='user', uselist=False, init=False, repr=False) 
    participant: Mapped[Optional["Participant"]] = relationship(back_populates='user', uselist=False, init=False, repr=False)


    @validates('role')
    def validate_role(self, key, role):
        if role not in Role:
            raise ValueError(f'invalid role value; Allowed values are: {[r.value for r in Role]}')
        return role



class Team(db.Model): # type: ignore
    team_id: Mapped[Optional[int]] = mapped_column(primary_key=True, autoincrement=True, init=False)
    leader_email: Mapped[str] = mapped_column(ForeignKey('participant.email'), nullable=False, init=False)
    event_id: Mapped[int] = mapped_column(ForeignKey('event.event_id'), nullable=False, init=False)

    leader: Mapped["Participant"] = relationship(back_populates='teams', init=True, repr=True)
    event: Mapped["Event"] = relationship(back_populates='teams', init=True, repr=True)



class TeamWiseMembers(db.Model): # type: ignore
    team_member_association_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, init=False)
    participant_email: Mapped[str] = mapped_column(ForeignKey('participant.email'), nullable=False, init=False)
    team_id: Mapped[int] = mapped_column(ForeignKey('team.team_id'), nullable=False, init=False)



class Participant(db.Model): # type: ignore
    email: Mapped[str] = mapped_column(ForeignKey('user.email'), primary_key=True, init=False)

    collage_name: Mapped[str] = mapped_column(String(32), nullable=False, init=True) # we can make StrEnum for this
    branch: Mapped[str] = mapped_column(String(32), nullable=False, init=True)

    user: Mapped["User"] = relationship(back_populates='participant', init=True, repr=True)
    teams: Mapped[List["Team"]] = relationship(back_populates='leader', init=False, repr=False)



class Event(db.Model): # type: ignore
    event_id: Mapped[Optional[int]] = mapped_column(primary_key=True, autoincrement=True, init=False)

    name: Mapped[str] = mapped_column(String(32), nullable=False, unique=True, init=True)
    branch: Mapped[str] = mapped_column(String(32), nullable=False, init=True)
    # prize: Mapped[Optional[Decimal]] = mapped_column(DECIMAL(10,2), nullable=True, init=True, default=None) 
    description: Mapped[str] = mapped_column(String(512), nullable=False, init=True)
    thumbnail: Mapped[str] = mapped_column(String(64), nullable=False, init=True) # we can add default thumbnail at app configuration and use that value here
    rules: Mapped[str] = mapped_column(nullable=False, init=True)
    last_modified_by: Mapped[str] = mapped_column(ForeignKey('user.email'), nullable=False, init=True)
    max_participants: Mapped[Optional[int]] = mapped_column(nullable=True, init=True, default=None)
    allow_registration: Mapped[bool] = mapped_column(nullable=False, init=True, default=True)
    created_at: Mapped[datetime.datetime] = mapped_column(nullable=False, init=False, default=datetime.datetime.now())
    last_modified_at: Mapped[datetime.datetime] = mapped_column(nullable=False, init=False, default=datetime.datetime.now())

    coordinators: Mapped[List["Coordinator"]] = relationship(back_populates='event', init=False, repr=False)
    teams: Mapped[List["Team"]] = relationship(back_populates='event', init=False, repr=False)

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



class EventWiseOrganizers(db.Model): # type: ignore
    event_organizer_association_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, init=False)
    organizer_email: Mapped[str] = mapped_column(ForeignKey('user.email'), nullable=False, init=False)
    event_id: Mapped[int] = mapped_column(ForeignKey('event.event_id'), nullable=False, init=False)



class Coordinator(db.Model): # type: ignore
    email: Mapped[str] = mapped_column(ForeignKey('user.email'), primary_key=True, init=False)
    event_id: Mapped[int] = mapped_column(ForeignKey('event.event_id'), nullable=False, init=False)

    user: Mapped["User"] = relationship(back_populates='coordinator', init=True, repr=True )
    event: Mapped["Event"] = relationship(back_populates='coordinators', init=True, repr=True)



class BranchAdmin(db.Model): # type: ignore
    email: Mapped[str] = mapped_column(ForeignKey('user.email'), primary_key=True, init=False)
    
    branch: Mapped[str] = mapped_column(String(32), unique=True, nullable=False, init=True)

    user: Mapped["User"] = relationship(back_populates='branch_admin', init=True, repr=True)

    @validates('branch')
    def validate_role(self, key, branch):
        if branch not in Branch:
            raise ValueError(f'invalid branch value; Allowed values are: {[r.value for r in Branch]}')
        return branch