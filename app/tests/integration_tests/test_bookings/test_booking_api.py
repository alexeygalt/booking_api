from datetime import date, datetime

import pytest
from httpx import AsyncClient


# @pytest.mark.parametrize("room_id,date_from,date_to,booked_rooms,status_code", [
#     *[(4, "2030-05-01", "2030-05-15", 201)] * 8,
#     (4, "2030-05-01", "2030-05-15", 409),
#     # (4, date(2030,5,1), date(2030,5,15), 200),
# ])
# @pytest.mark.parametrize("room_id,date_from,date_to,booked_rooms,status_code", *[
#     [(4, "2030-05-01", "2030-05-15", i, 201) for i in range(3, 11)] +
#     [(4, "2030-05-01", "2030-05-15", 10, 409)] * 2
# ])
@pytest.mark.parametrize("room_id,date_from,date_to,booked_rooms,status_code", [
    (4, "2030-05-01", "2030-05-15", 3, 201),
    (4, "2030-05-02", "2030-05-16", 4, 201),
    (4, "2030-05-03", "2030-05-17", 5, 201),
    (4, "2030-05-04", "2030-05-18", 6, 201),
    (4, "2030-05-05", "2030-05-19", 7, 201),
    (4, "2030-05-06", "2030-05-20", 8, 201),
    (4, "2030-05-07", "2030-05-21", 9, 201),
    (4, "2030-05-08", "2030-05-22", 10, 201),
    (4, "2030-05-09", "2030-05-23", 10, 409),
    (4, "2030-05-10", "2030-05-24", 10, 409),
])
async def test_add_and_get_booking(room_id, date_from, date_to, status_code, booked_rooms,
                                   authenticated_ac: AsyncClient):
    response = await authenticated_ac.post("/bookings", json={
        "room_id": room_id,
        "date_from": date_from,
        "date_to": date_to,
    })

    assert response.status_code == status_code
    temp = await authenticated_ac.get("/bookings")
    assert len(temp.json()) == booked_rooms


@pytest.mark.parametrize("room_id,date_from,date_to,status_code", [
    (4, "2030-05-01", "2030-05-01", 400),
    (4, "2030-05-01", "2030-06-16", 400),
])
async def test_add_and_get_booking_with_wrong_date(room_id, date_from, date_to, status_code,
                                                   authenticated_ac: AsyncClient):
    response = await authenticated_ac.post("/bookings", json={
        "room_id": room_id,
        "date_from": date_from,
        "date_to": date_to,
    })
    assert response.status_code == status_code


async def test_get_bookings_and_clear(authenticated_ac: AsyncClient):
    response = await authenticated_ac.get("/bookings")
    for id in [item['id'] for item in response.json()]:
        temp = await authenticated_ac.delete(f"/bookings/{id}")
    response = await authenticated_ac.get("/bookings")
    assert len(response.json()) == 0
