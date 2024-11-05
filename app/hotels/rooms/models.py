from typing import Optional

from sqlalchemy import JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Rooms(Base):
    __tablename__ = "rooms"
    # id = Column(Integer, primary_key=True)
    # hotel_id = Column(ForeignKey("hotels.id"), nullable=False)
    # name = Column(String, nullable=False)
    # description = Column(String, nullable=True)
    # price = Column(Integer, nullable=False)
    # services = Column(JSON, nullable=True)
    # quantity = Column(Integer, nullable=False)
    # image_id = Column(Integer)
    id: Mapped[int] = mapped_column(primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"))
    name: Mapped[str]
    description: Mapped[Optional[str]]
    price: Mapped[int]
    services: Mapped[Optional[list[str]]] = mapped_column(JSON)
    quantity: Mapped[int]
    image_id: Mapped[int]

    hotel = relationship("Hotels", back_populates="rooms")
    booking = relationship("Bookings", back_populates="room")

    def __str__(self):
        return f"Number {self.name}"
