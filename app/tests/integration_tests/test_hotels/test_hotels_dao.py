from datetime import date, datetime

from app.hotels.dao import HotelsDAO
from app.hotels.schemas import SHotelCreate


async def test_find_all_hotels():
    hotels = await HotelsDAO.find_all(
        location="Алтай",
        date_from=datetime.strptime("2023-07-10", "%Y-%m-%d"),
        date_to=datetime.strptime("2023-07-24", "%Y-%m-%d")
    )
    assert len(hotels) > 0


async def test_find_hotel_by_id():
    hotel = await HotelsDAO.find_by_id(model_id=1)
    assert hotel.name == "Cosmos Collection Altay Resort"


async def test_add__hotel():
    hotel_data = {
        "name": "test_hotel",
        "location": "test location",
        "services": ["some services"],
        "rooms_quantity": 322,
        "image_id": 1
    }
    hotel_data = SHotelCreate(**hotel_data)
    new_hotel = await HotelsDAO.add(hotel_data)
    assert new_hotel.id is not None


async def test_get_hotel_rooms():
    rooms = await HotelsDAO.get_hotel_rooms(hotel_id=1, date_from=date(2030, 1, 1), date_to=date(2030, 1, 20))
    assert len(rooms) == 2
