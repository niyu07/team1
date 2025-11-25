from sqlalchemy import Column, Integer, String, Boolean
from .database import Base


class Item(Base):
    __tablename__ = "item"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    date = Column(String, index=True)
    detail = Column(String, index=True)
    tag = Column(String, index=True)
    state = Column(Boolean, index=True)


