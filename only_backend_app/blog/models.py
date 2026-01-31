from sqlalchemy import ForeignKey
from .database import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship
from typing import List

class Blog(Base):
    __tablename__='blog'
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    body: Mapped[str] 
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    
    user: Mapped['User'] = relationship(back_populates='blogs')

    def __repr__(self) -> str:
        return f"Blog(id={self.id!r}, title={self.title!r}, body={self.body!r}, user_id={self.user_id!r})"

class User(Base):
    __tablename__='user'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    email: Mapped[str] 
    password: Mapped[str]

    blogs: Mapped[List['Blog']]= relationship(back_populates='user')