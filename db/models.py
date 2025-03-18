from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from db.base import Base


class Gift(Base):
    __tablename__ = "gifts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    username = Column(String, nullable=False)
    gift_name = Column(String, nullable=False)
    gift_model = Column(String, nullable=False)
    gift_background = Column(String, nullable=True)
    gift_color = Column(String, nullable=True)
    gift_pattern = Column(String, nullable=True)
    price = Column(Float, nullable=True)
    created_at = Column(DateTime, default=func.now())
    post_id = Column(Integer, nullable=True)
