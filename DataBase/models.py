from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Table, DATETIME

Base = declarative_base()

tag_post = Table(
    'tag_post',
    Base.metadata,
    Column("post_id", Integer, ForeignKey("post.id")),
    Column("tag_id", Integer, ForeignKey("tag.id"))
)


class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    url = Column(String, nullable=False, unique=True)
    title = Column(String, nullable=False)
    image = Column(String, unique=True)
    publicationdate = Column(DATETIME)
    countcomments = Column(Integer, nullable=False, default=0)
    timeread = Column(String, nullable=False, default="5 минут")
    views = Column(Integer, nullable=False, default=0)
    commentable_id = Column(Integer)
    author_id = Column(Integer, ForeignKey("author.id"))
    author = relationship("Author")
    tags = relationship("Tag", secondary=tag_post)


class Author(Base):
    __tablename__ = 'author'
    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    url = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False)
    post = relationship("Post")


class Tag(Base):
    __tablename__ = 'tag'
    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    url = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False)
    posts = relationship("Post", secondary=tag_post)
