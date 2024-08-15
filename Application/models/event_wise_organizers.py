from Application import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

class EventWiseOrganizers(db.Model): # type: ignore
    event_organizer_association_id = mapped_column(primary_key=True, autoincrement=True, init=False)
    organizer_email: Mapped[str] = mapped_column(ForeignKey('user.email'), nullable=False, init=False)
    event_id: Mapped[int] = mapped_column(ForeignKey('event.event_id'), nullable=False, init=False)