from pydantic import BaseModel


class SHotels(BaseModel):
    id: int
    name: str
    location: str
    services: list[str]
    rooms_quantity: int
    image_id: int

    class Config:
        from_attributes = True


class SHotelCreate(BaseModel):
    name: str
    location: str
    services: list[str]
    rooms_quantity: int
    image_id: int | None

    class Config:
        from_attributes = True


class HotelsListOutput(BaseModel):
    id: int
    name: str
    location: str
    services: list[str]
    rooms_quantity: int
    image_id: int
    rooms_left: int
