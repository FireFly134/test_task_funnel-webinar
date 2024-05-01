import os
from datetime import timedelta

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func

login = os.getenv("POSTGRES_USER", "")
passwd = os.getenv("POSTGRES_PASSWORD", "")
name_db = os.getenv("POSTGRES_DB", "")
url_engine = f"postgresql://{login}:{passwd}@postgres-db:5432/{name_db}"

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True

    id = Column(
        Integer,
        nullable=False,
        unique=True,
        primary_key=True,
        autoincrement=True,
    )
    created_at = Column(DateTime, default=func.now())
    status_updated_at = Column(
        DateTime, default=func.now(), onupdate=func.now()
    )
    status = Column(String, default="alive")


class User(BaseModel):
    __tablename__ = "users_test"
    user_id = Column(String, default="0")
    next_time_msg = Column(DateTime, default=func.now() + timedelta(days=1))
    count_msg = Column(Integer, default=1)
    stop_word = Column(Boolean, default=False)
    send_msg = Column(Boolean, default=False)

    def __repr__(self):
        return (
            "id|user_id|created_at|status_updated_at|status|"
            "next_time_msg|count_msg|stop_word|send_msg|"
            f"{self.id}|{self.user_id}|{self.created_at}|"
            f"{self.status_updated_at}|{self.status}|{self.next_time_msg}|"
            f"{self.count_msg}|{self.stop_word}|{self.send_msg}|"
        )
