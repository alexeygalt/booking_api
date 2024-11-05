from datetime import date
from fastapi import APIRouter, Depends
from app.hotels.dao import HotelsDAO
from app.hotels.rooms.schemas import SRoomList
from app.hotels.schemas import HotelsListOutput, SHotelCreate, SHotels
from app.users.dependencies import get_current_user
from app.users.models import Users

router = APIRouter(prefix="/hotels", tags=["Hotels"])


@router.get("/{location}")
# @cache(expire=60)
async def get_hotels(
    location: str, date_from: date, date_to: date
) -> list[HotelsListOutput]:
    return await HotelsDAO.find_all(location, date_from, date_to)


@router.get("/id/{hotel_id}")
async def get_hotel(hotel_id: int) -> SHotels:
    return await HotelsDAO.find_by_id(hotel_id)


@router.post("")
async def add_hotel(hotel_data: SHotelCreate, user: Users = Depends(get_current_user)):
    return await HotelsDAO.add(hotel_data)


@router.delete("/{hotel_id}")
async def delete_hotel(hotel_id: int, user: Users = Depends(get_current_user)):
    return await HotelsDAO.delete(id=hotel_id)


@router.get("/{hotel_id}/rooms")
async def get_hotel_rooms(
    hotel_id: int, date_from: date, date_to: date
) -> list[SRoomList]:
    return await HotelsDAO.get_hotel_rooms(hotel_id, date_from, date_to)
