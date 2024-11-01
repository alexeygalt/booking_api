# Booking Service

This is a booking service built with FastAPI. It enables users to manage bookings and uses PostgreSQL for database
storage. The service includes background task processing with Celery and Redis.

## Technology Stack

- **FastAPI** — for building the REST API.
- **SQLAlchemy** — as an ORM for database interactions.
- **Alembic** — for handling database migrations.
- **PostgreSQL** — as the database.
- **Celery** — for background task processing.
- **Redis** — as the message broker for Celery.

## Features

- CRUD (Create, Read, Update, Delete) operations for managing bookings.
- Background task handling with Celery and Redis.

## Installation

### Prerequisites

Ensure you have the following installed on your system:

- Python 3.8+
- PostgreSQL
- Redis

### Setup

1. **Clone the repository**:

   ```bash
   git clone https://github.com/alexeygalt/booking_api
   cd booking-service
   ```

2. **Set up a virtual environment**:

```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install dependencies:**:
   Create a .env file with the following variables