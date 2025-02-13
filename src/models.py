import os
import enum
from sqlalchemy.orm import relationship, declarative_base, Mapped, mapped_column
from sqlalchemy import create_engine, ForeignKey, String, Column, Table, Enum
from eralchemy2 import render_er

Base = declarative_base()

followers = Table(
    "followers",
    Base.metadata,
    Column("user_from_id", ForeignKey("users.id")),
    Column("users_to_id", ForeignKey("users.id")),
)

class Users(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False)
    firstname: Mapped[str] = mapped_column(nullable=False)
    lastname: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(String(80), nullable=False, unique=True)
    post: Mapped["Post"] = relationship(back_populates="users")
    comment: Mapped["Comment"] = relationship(back_populates="users")

class Post(Base):
    __tablename__ = 'post'
    id: Mapped[int] = mapped_column(primary_key=True)
    users_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    users: Mapped["Users"] = relationship(back_populates="post")
    comment: Mapped["Comment"] = relationship(back_populates="post")
    media: Mapped["Media"] = relationship(back_populates="post")

class Comment(Base):
    __tablename__ = 'comment'
    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(nullable=False)
    users_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    users: Mapped["Users"] = relationship(back_populates="comment")
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))
    post: Mapped["Post"] = relationship(back_populates="comment")

class MyEnum(enum.Enum):
    image = ".img"
    video = ".mp4"

class Media(Base):
    __tablename__ = 'media'
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[MyEnum] = mapped_column(nullable=False)
    url: Mapped[str] = mapped_column(nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))
    post: Mapped["Post"] = relationship(back_populates="media")


    def to_dict(self):
        return {}

## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e
