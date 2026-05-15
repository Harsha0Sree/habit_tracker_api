# Habit Tracker API

A lightweight REST API built with FastAPI and SQLite for tracking habits.

## Features

* Create habits
* Retrieve all habits
* Retrieve a single habit
* Update habits
* Delete habits
* SQLite persistence
* FastAPI automatic Swagger documentation

---

## Tech Stack

* Python
* FastAPI
* SQLite
* Pydantic

---

## Project Structure

```bash
habit-tracker-api/
│
├── app/
│   ├── main.py
│   ├── routes/
│   ├── schemas/
│   ├── services/
│   ├── models/
│   └── database/
│
├── data.db
├── README.md
├── requirements.txt
└── .gitignore
```

---

## Installation

Clone the repository:

```bash
git clone <repo-url>
cd habit-tracker-api
```

Create virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Running the Server

```bash
uvicorn app.main:app --reload
```

Server runs on:

```text
http://127.0.0.1:8000
```

---

## API Documentation

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

ReDoc:

```text
http://127.0.0.1:8000/redoc
```

---

## API Endpoints

### Create Habit

```http
POST /habits
```

Request Body:

```json
{
  "name": "Workout",
  "logs": "daily"
}
```

---

### Get All Habits

```http
GET /habits
```

---

### Get Single Habit

```http
GET /habits/{name}
```

---

### Update Habit

```http
PUT /habits/{name}
```

Request Body:

```json
{
  "name": "Workout",
  "name_to_update_to": "Gym"
}
```

---

### Delete Habit

```http
DELETE /habits/{name}
```

---

## Future Improvements

* SQLAlchemy ORM
* Authentication
* Docker support
* PostgreSQL migration
* Habit streak tracking
* Unit tests
* Async database support

---

## License

MIT
