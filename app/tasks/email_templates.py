from email.message import EmailMessage

from pydantic import EmailStr

from app.config import settings


def create_booking_confirmation_template(booking: dict, email_to: EmailStr):
    email = EmailMessage()
    email["Subject"] = "Booking approve"
    email["From"] = settings.EMAIL_HOST_USER
    email["To"] = email_to

    email.set_content(
        f"""
        <h1>Confirm your reservation</h1>
        You have booked a room from {booking["date_from"]} to {booking["date_to"]}
        """,
        subtype="html",
    )
    return email
