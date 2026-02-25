from sqlalchemy import text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base, str_uniq, int_pk, str_null_true
from typing import List



class Major(Base):
    id: Mapped[int_pk]
    major_name: Mapped[str_uniq]
    major_description: Mapped[str_null_true]
    students_count: Mapped[int] = mapped_column(server_default=text('0'))

    students: Mapped[List['Student']] = relationship('Student', back_populates='major')

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id}, major_name={self.major_name!r})"
    