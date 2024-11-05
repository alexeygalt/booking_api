from datetime import date

from sqlalchemy import and_, delete, func, insert, or_, select
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import SQLAlchemyError
from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.exceptions import InvalidDateToBooking
from app.hotels.rooms.models import Rooms
from app.logger import logger


class BookingDAO(BaseDAO):
    model = Bookings

    @classmethod
    async def add(cls, user_id, room_id: int, date_from: date, date_to: date):
        if date_to < date_from:
            raise InvalidDateToBooking
        session: Session
        try:
            async with async_session_maker() as session:
                booked_rooms = (
                    select(Bookings)
                    .where(
                        and_(
                            Bookings.room_id == room_id,
                            or_(
                                and_(
                                    Bookings.date_from >= date_from,
                                    Bookings.date_from <= date_to,
                                ),
                                and_(
                                    Bookings.date_from <= date_from,
                                    Bookings.date_to > date_from,
                                ),
                            ),
                        )
                    )
                    .cte("booked_rooms")
                )

                get_rooms_left = (
                    select(
                        (
                            Rooms.quantity
                            - func.count(booked_rooms.c.room_id).filter(
                                booked_rooms.c.room_id.is_not(None)
                            )
                        ).label("rooms_left")
                    )
                    .select_from(Rooms)
                    .join(
                        booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True
                    )
                    .where(Rooms.id == room_id)
                    .group_by(Rooms.quantity, booked_rooms.c.room_id)
                )
                rooms_left = await session.execute(get_rooms_left)
                rooms_left = rooms_left.scalar()
                if rooms_left > 0:
                    get_price = select(Rooms.price).filter_by(id=room_id)
                    price = await session.execute(get_price)
                    price: int = price.scalar()
                    add_booking = (
                        insert(Bookings)
                        .values(
                            room_id=room_id,
                            user_id=user_id,
                            date_from=date_from,
                            date_to=date_to,
                            price=price,
                        )
                        .returning(Bookings)
                    )
                    new_booking = await session.execute(add_booking)
                    await session.commit()
                    # return new_booking.mappings().one()
                    return new_booking.scalar()

                else:
                    return None
        except (SQLAlchemyError, Exception) as e:
            if isinstance(e, SQLAlchemyError):
                msg = "Database Exc"
            elif isinstance(e, Exception):
                msg = "Unknown Exc"
            msg += ": Cannot add booking"
            logger.error(
                msg,
                extra={
                    "user_id": user_id,
                    "room_id": room_id,
                    "date_from": date_from,
                    "date_to": date_to,
                },
                exc_info=True,
            )

    @classmethod
    async def find_all(cls, user_id: int):
        session: Session
        async with (async_session_maker() as session):
            query = (
                select(
                    Bookings.id,
                    Bookings.user_id,
                    Bookings.date_from,
                    Bookings.date_to,
                    Bookings.price,
                    Bookings.total_cost,
                    Bookings.total_days,
                    Rooms.image_id,
                    Rooms.name,
                    Rooms.description,
                    Rooms.services,
                )
                .select_from(Bookings)
                .join(Rooms, Rooms.id == Bookings.room_id)
                .where(Bookings.user_id == user_id)
            )

            result = await session.execute(query)
            return result.mappings().all()

    @classmethod
    async def delete(cls, booking_id, user_id):
        session: Session
        async with async_session_maker() as session:
            # query = select(cls.model).filter_by(id=booking_id)
            # result = await session.execute(query)
            # booking = result.mappings().all()
            # if not booking:
            #     return None

            if not await cls.find_one_or_none(id=booking_id, user_id=user_id):
                return False
            query = delete(cls.model).filter_by(id=booking_id)
            await session.execute(query)
            await session.commit()
            return True
