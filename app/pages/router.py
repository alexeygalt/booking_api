import json
from datetime import date, datetime, timedelta

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.bookings.dao import BookingDAO
from app.bookings.router import add_booking, get_all_bookings
from app.hotels.router import get_hotel, get_hotel_rooms, get_hotels
from app.users.dependencies import get_current_user
from app.users.models import Users
from app.utils import format_number_thousand_separator, get_month_days

router = APIRouter(prefix="/pages", tags=["Frontend"])

templates = Jinja2Templates(directory="app/templates")


@router.get('/')
async def get_main(request: Request):
    return templates.TemplateResponse(name="base.html", context={"request": request, })


@router.get('/hotels')
async def get_hotels_page(request: Request, hotels=Depends(get_hotels)):
    return templates.TemplateResponse(name="hotels.html", context={"request": request, "hotels": hotels})


@router.get("/login", response_class=HTMLResponse)
async def get_login_page(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request": request})


@router.get("/register", response_class=HTMLResponse)
async def get_register_page(request: Request):
    return templates.TemplateResponse("auth/register.html", {"request": request})


@router.get("/bookings", response_class=HTMLResponse)
async def get_bookings_page(
        request: Request,
        bookings=Depends(get_all_bookings),
):
    return templates.TemplateResponse(
        "bookings/bookings.html",
        {
            "request": request,
            "bookings": bookings,
            "format_number_thousand_separator": format_number_thousand_separator,
        },
    )


@router.get("/hotels/{location}", response_class=HTMLResponse)
async def get_hotels_page(
        request: Request,
        location: str,
        date_to: date,
        date_from: date,
        hotels=Depends(get_hotels),
):
    dates = get_month_days()
    if date_from > date_to:
        date_to, date_from = date_from, date_to
    # Автоматически ставим дату заезда позже текущей даты
    date_from = max(datetime.today().date(), date_from)
    # Автоматически ставим дату выезда не позже, чем через 180 дней
    date_to = min((datetime.today() + timedelta(days=180)).date(), date_to)
    return templates.TemplateResponse(
        "hotels_and_rooms/hotels.html",
        {
            "request": request,
            "hotels": hotels,
            "location": location,
            "date_to": date_to.strftime("%Y-%m-%d"),
            "date_from": date_from.strftime("%Y-%m-%d"),
            "dates": dates,
        },
    )


@router.get("/hotels/{hotel_id}/rooms", response_class=HTMLResponse)
async def get_rooms_page(
        request: Request,
        date_from: date,
        date_to: date,
        rooms=Depends(get_hotel_rooms),
        hotel=Depends(get_hotel),
):
    date_from_formatted = date_from.strftime("%d.%m.%Y")
    date_to_formatted = date_to.strftime("%d.%m.%Y")
    booking_length = (date_to - date_from).days
    return templates.TemplateResponse(
        "hotels_and_rooms/rooms.html",
        {
            "request": request,
            "hotel": hotel,
            "rooms": rooms,
            "date_from": date_from,
            "date_to": date_to,
            "booking_length": booking_length,
            "date_from_formatted": date_from_formatted,
            "date_to_formatted": date_to_formatted,
        },
    )


@router.post("/successful_booking", response_class=HTMLResponse)
async def get_successful_booking_page(
        request: Request,
        # _=Depends(add_booking),
        date_from: date = Form(...),
        date_to: date = Form(...),
        room_id: int = Form(...),
        user: Users = Depends(get_current_user)

):
    await BookingDAO.add(user_id=user.id, date_from=date_from, date_to=date_to, room_id=room_id)

    return templates.TemplateResponse(
        "bookings/booking_successful.html", {"request": request}
    )


@router.post("/successful_delete", response_class=HTMLResponse)
async def get_delete_booking(
        request: Request,
        booking_id: int = Form(...),
        user: Users = Depends(get_current_user)
):
    await BookingDAO.delete(user_id=user.id,booking_id=booking_id)
    return templates.TemplateResponse(
        "bookings/booking_delete.html", {"request": request}
    )