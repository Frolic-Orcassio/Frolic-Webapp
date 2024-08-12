from Application import db, Role
from sqlalchemy.orm import Mapped, mapped_column, validates, relationship
from sqlalchemy import String
from typing import Optional

class User(db.Model): # type: ignore
    email: Mapped[str] = mapped_column(String(320), primary_key=True, init=True)
    name: Mapped[str] = mapped_column(String(64), nullable=False, init=True)
    dp: Mapped[str] = mapped_column(String(64), nullable=True, init=False)
    role: Mapped[str] = mapped_column(String(16), nullable=False, init=False, default=Role.PARTICIPANT)
    is_authenticated: Mapped[bool] = mapped_column(nullable=False, init=True)

    branch_admin: Mapped[Optional["BranchAdmin"]] = relationship(back_populates='user', uselist=False, init=False, repr=False) # type: ignore
    coordinator: Mapped[Optional["Coordinator"]] = relationship(back_populates='user', uselist=False, init=False, repr=False) # type: ignore


    @validates('role')
    def validate_role(self, key, role):
        if role not in Role:
            raise ValueError(f'invalid role value; Allowed values are: {[r.value for r in Role]}')
        return role