import pytest
from httpx import AsyncClient


async def test_add_and_get_hotel(authenticated_ac: AsyncClient):
    response = await authenticated_ac.post(
        "/hotels",
        json={
            "name": "test_hotel",
            "location": "test location",
            "services": ["some services"],
            "rooms_quantity": 322,
            "image_id": 1,
        },
    )
    assert response.status_code == 200
    response = await authenticated_ac.get("hotels/id/7")
    assert response.json()["name"] == "test_hotel"


@pytest.mark.parametrize(
    "location,date_from,date_to",
    [
        ("Алтай", "2023-05-01", "2023-05-30"),
    ],
)
async def test_get_hotel_by_location(
    location, date_from, date_to, authenticated_ac: AsyncClient
):
    response = await authenticated_ac.get(
        f"/hotels/{location}",
        params={
            "date_from": date_from,
            "date_to": date_to,
        },
    )
    assert len(response.json()) == 3


@pytest.mark.parametrize(
    "hotel_id,date_from,date_to",
    [
        (1, "2030-05-01", "2030-05-20"),
    ],
)
async def test_get_hotel_rooms(
    hotel_id, date_from, date_to, authenticated_ac: AsyncClient
):
    response = await authenticated_ac.get(
        f"/hotels/{hotel_id}/rooms",
        params={
            "date_from": date_from,
            "date_to": date_to,
        },
    )
    assert len(response.json()) == 2
