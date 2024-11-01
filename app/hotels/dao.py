from datetime import date

from sqlalchemy import and_, func, insert, or_, select
from sqlalchemy.orm import Session

from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from app.database import async_session_maker, engine
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms
from app.hotels.schemas import SHotelCreate


class HotelsDAO(BaseDAO):
    model = Hotels

    @classmethod
    async def add(cls, hotel_data: SHotelCreate):
        async with async_session_maker() as session:
            query = insert(cls.model).values(**hotel_data.model_dump()).returning(Hotels)
            result = await session.execute(query)
            await session.commit()
            return result.scalar()

    @classmethod
    async def find_all(cls, location: str, date_from: date, date_to: date):
        session: Session
        async with async_session_maker() as session:
            booked_rooms = (
                select(Hotels.id.label("hotel_id"), Bookings.room_id, func.count(Hotels.id).label("booked_rooms")
                       ).select_from(Hotels).join(Rooms, Hotels.id == Rooms.hotel_id
                                                  ).join(Bookings,
                                                         Rooms.id == Bookings.room_id).where(
                    or_(
                        and_(
                            Bookings.date_from >= date_from,
                            Bookings.date_from <= date_to,
                        ),
                        and_(
                            Bookings.date_from <= date_from,
                            Bookings.date_to > date_from,
                        ),
                    ))).group_by(Hotels.id, Bookings.room_id).cte("booked_rooms")

            filtered_hotels = select(Hotels.id, Hotels.name, Hotels.location, Hotels.services, Hotels.rooms_quantity,
                                     Hotels.image_id,
                                     (Hotels.rooms_quantity - func.coalesce(booked_rooms.c.booked_rooms, 0)).label(
                                         "rooms_left")
                                     ).select_from(
                Hotels).join(booked_rooms, booked_rooms.c.hotel_id == Hotels.id, isouter=True).filter(
                Hotels.location.like(f"%{location}%")).cte("filtered_hotels")

            temp = select(filtered_hotels).filter(filtered_hotels.c.rooms_left >= 1)

            result = await session.execute(temp)
            return result.mappings().all()

    # @classmethod
    # async def get_hotel_rooms(cls, hotel_id: int):
    #     async with async_session_maker() as session:
    #         query = select(Rooms).filter(Rooms.hotel_id == hotel_id)
    #         result = await session.execute(query)
    #         return result.scalars().all()
    @classmethod
    async def get_hotel_rooms(cls, hotel_id: int, date_from: date, date_to: date):
        async with async_session_maker() as session:
            booked_rooms = select(Bookings.room_id, func.count(Rooms.id).label("booked_count")).select_from(
                Rooms).join(
                Bookings, Rooms.id == Bookings.room_id
            ).where(
                or_(
                    and_(
                        Bookings.date_from >= date_from,
                        Bookings.date_from <= date_to,
                    ),
                    and_(
                        Bookings.date_from <= date_from,
                        Bookings.date_to > date_from,
                    ),
                )).group_by(Bookings.room_id).cte("booked_rooms")
            # print(booked_rooms.compile(engine, compile_kwargs={"literal_binds": True}))

            filtered_rooms = select(Rooms.id, Rooms.hotel_id, Rooms.name, Rooms.description, Rooms.services,
                                    Rooms.price, Rooms.quantity, Rooms.image_id,
                                    ((date_to - date_from).days * Rooms.price).label("total_cost"),
                                    (Rooms.quantity - func.coalesce(booked_rooms.c.booked_count, 0)).label("rooms_left")).select_from(
                Rooms).join(booked_rooms,
                            booked_rooms.c.room_id == Rooms.id,
                            full=True).where(
                Rooms.hotel_id == hotel_id)

            result = await session.execute(filtered_rooms)
            return result.mappings().all()




            # with booked_rooms as (
            # select room_id, count(*) as booked_count from rooms
            # join bookings on bookings.room_id = rooms.id
            # WHERE (bookings.date_from >= '2023-05-15' AND bookings.date_from <= '2023-06-20') OR
            #       (bookings.date_from <= '2023-05-15' AND bookings.date_to > '2023-05-15')
            # group by room_id)
            #
            #
            # select *,(date_to - date_from) * price  as cost, quantity - coalesce(booked_rooms.booked_count,0) as rooms_left from rooms
            # full join   booked_rooms on booked_rooms.room_id = rooms.id
            # where rooms.hotel_id = 1
