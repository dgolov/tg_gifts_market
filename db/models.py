from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from db.engine import Base


class Gift(Base):
    __tablename__ = "gifts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    username = Column(String, nullable=False)
    owner = Column(String, nullable=True)
    name = Column(String, nullable=False)
    number = Column(Integer, nullable=True)
    model = Column(String, nullable=False)
    background = Column(String, nullable=True)
    symbol = Column(String, nullable=True)
    price = Column(Float, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now())
    post_id = Column(Integer, nullable=True)
    url = Column(String, nullable=False)
