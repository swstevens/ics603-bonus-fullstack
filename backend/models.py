"""
Database models
"""
from sqlalchemy import Column, Integer, String, DateTime, Text, Table, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

reflection_topics = Table(
    'reflection_topics',
    Base.metadata,
    Column('reflection_id', Integer, ForeignKey('reflections.id'), primary_key=True),
    Column('topic_id', Integer, ForeignKey('topics.id'), primary_key=True)
)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    reflections = relationship("Reflection", back_populates="user")
    topics = relationship("Topic", back_populates="user")

class Topic(Base):
    __tablename__ = "topics"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="topics")
    reflections = relationship("Reflection", secondary=reflection_topics, back_populates="topic_list")

class Reflection(Base):
    __tablename__ = "reflections"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    text = Column(Text, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="reflections")
    topic_list = relationship("Topic", secondary=reflection_topics, back_populates="reflections")
