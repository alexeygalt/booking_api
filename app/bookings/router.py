from datetime import date, timedelta

from fastapi import APIRouter, Depends, Response
from fastapi.responses import JSONResponse
from pydantic import parse_obj_as

from app.bookings.dao import BookingDAO
from app.bookings.schemas import SBooking, SBookingList, SNewBooking
from app.exceptions import InvalidDateToBooking, RoomCannotBeBooked
from app.tasks.tasks import send_booking_confirmation_email
from app.users.dependencies import get_current_user
from app.users.models import Users

router = APIRouter(prefix='/bookings', tags=['Bookings'])


# @router.post("")
# async def add_booking(
#         room_id: int, date_from: date, date_to: date,
#         user: Users = Depends(get_current_user)
# ):
#     booking = await BookingDAO.add(user.id, room_id, date_from, date_to)
#     if not booking:
#         raise RoomCannotBeBooked
@router.post("", status_code=201)
async def add_booking(
        booking: SNewBooking,
        user: Users = Depends(get_current_user),
):
    if (booking.date_from >= booking.date_to) or (booking.date_to - booking.date_from > timedelta(days=30)):
        raise InvalidDateToBooking
    booking = await BookingDAO.add(
        user.id,
        booking.room_id,
        booking.date_from,
        booking.date_to,
    )
    if not booking:
        raise RoomCannotBeBooked
    booking_dict = SBooking.model_validate(booking).model_dump()
    # booking_dict = parse_obj_as(SBooking,booking).dict()
    # booking_dict = SBooking(**booking)
    # print(booking_dict)
    send_booking_confirmation_email.delay(booking_dict, user.email)
    # print(user.email)
    return booking


@router.get("")
async def get_all_bookings(user: Users = Depends(get_current_user)) -> list[SBookingList]:
    return await BookingDAO.find_all(user_id=user.id)


@router.delete("/{booking_id}")
async def delete_booking(booking_id: int, user: Users = Depends(get_current_user)):
    if not await BookingDAO.delete(booking_id=booking_id, user_id=user.id):
        return JSONResponse(status_code=400, content="Object not found")
    return Response(status_code=204)
