from Application import db, Branch
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from sqlalchemy import String, ForeignKey
from typing import Optional

class BranchAdmin(db.Model): # type: ignore
    email: Mapped[str] = mapped_column(ForeignKey('user.email'), primary_key=True, init=False)
    branch: Mapped[str] = mapped_column(String(32), unique=True, nullable=False, init=True)

    user: Mapped["User"] = relationship(back_populates='branch_admin', init=True, repr=True) # type: ignore

    @validates('branch')
    def validate_role(self, key, branch):
        if branch not in Branch:
            raise ValueError(f'invalid branch value; Allowed values are: {[r.value for r in Branch]}')
        return branch