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
- **Prometheus** — for monitoring application metrics.
- **Grafana** — for visualizing metrics and monitoring dashboards.

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

3. Create an `.env` file in the project root directory based on the `.env.example` template:
   ```bash
   cp .env.example .env
   ```

4. To start the application, run:

```bash
   uvicorn app.main:app --reload --port 8000  
```

#### Run with Docker

Create an `.env-non-dev` file in the project root directory based on the `.env-non-dev.example` template:

```bash
   docker-compose up -d
```


## Usage

- **API Endpoints**: You can access the API endpoints via [http://localhost:8000](http://localhost:8000). Detailed API
  documentation is available through FastAPI's built-in Swagger
  at [http://localhost:8000/docs](http://localhost:8000/docs).


## Testing
```bash
   pytest
```



markdown
Копировать код
## Monitoring & Error Tracking

The project is set up to use **Sentry** for error monitoring. Configure Sentry by setting the `SENTRY_DSN` in the `.env` file.

For system metrics and performance monitoring, **Prometheus** and **Grafana** are integrated into the project:

- **Prometheus** collects metrics from the FastAPI application, Celery tasks, and other services, providing detailed insights into resource usage and application behavior over time.
- **Grafana** is used for visualizing these metrics, allowing for the creation of customizable dashboards and setting up alerts based on defined thresholds to help proactively monitor system health.

To enable Prometheus and Grafana monitoring, ensure the services are correctly configured in `docker-compose.yml` and started alongside the application.