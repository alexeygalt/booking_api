from typing import Optional

from sqlalchemy import JSON, Column, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Hotels(Base):
    __tablename__ = 'hotels'
    # id = Column(Integer, primary_key=True)
    # name = Column(String, nullable=False)
    # location = Column(String, nullable=False)
    # services = Column(JSON)
    # rooms_quantity = Column(Integer, nullable=False)
    # image_id = Column(Integer)
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    location: Mapped[str]
    services: Mapped[list[str]] = mapped_column(JSON)
    rooms_quantity: Mapped[int]
    image_id: Mapped[int]

    rooms = relationship("Rooms",back_populates='hotel')

    def __str__(self):
        return self.name





