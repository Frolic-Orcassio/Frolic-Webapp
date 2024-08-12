from Application import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

class Coordinator(db.Model): # type: ignore
    email: Mapped[str] = mapped_column(ForeignKey('user.email'), primary_key=True, init=False)
    event_name: Mapped[str] = mapped_column(ForeignKey('event.name'), nullable=False, init=False)

    user: Mapped["User"] = relationship(back_populates='coordinator', init=True, repr=True ) # type: ignore
    event: Mapped["Event"] = relationship(back_populates='coordinators', init=True, repr=True) # type: ignore