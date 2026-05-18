import sqlite3
from datetime import date
from database import SessionLocal,Base,engine
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from models import Habit
from pydantic import BaseModel
from sqlalchemy import select

DATABASE = "data.db"

Base.metadata.create_all(engine)


class HabitCreate(BaseModel):
    name: str


class HabitToUpdate(BaseModel):
    name: str
    name_to_update_to: str


def create_habit_table(DATABASE):
    with DatabaseConnection(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS habits   (
                        id INTEGER PRIMARY KEY,
                        name TEXT UNIQUE NOT NULL,
                        created_at TEXT,
                        description TEXT
                                
                )
                """)


def create_logs_table(DATABASE):
    with DatabaseConnection(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        cursor.execute("""CREATE TABLE IF NOT EXISTS logs(
                       id INTEGER PRIMARY KEY,
                       log_date TEXT NOT NULL,
                       habit_id INTEGER NOT NULL,
                       FOREIGN KEY (habit_id) REFERENCES habits(id)
                       ON DELETE CASCADE
                       )
                        """)


class DatabaseConnection:
    def __init__(self, database_path):
        self.database_path = database_path
        self.conn = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.database_path)
        self.conn.row_factory = sqlite3.Row
        return self.conn

    def __exit__(self, exc_type, exc, tb):
        if self.conn:
            if exc_type is None:
                self.conn.commit()
            else:
                self.conn.rollback()
            self.conn.close()


create_habit_table(DATABASE)
create_logs_table(DATABASE)
app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def home():
    return {"message": "the table has been created and running"}


@app.get("/dashboard")
def get_dashboard(request: Request):
    with SessionLocal() as session:
        row = select(Habit)
        habits = session.execute(row).scalars().all()
        return templates.TemplateResponse(
            request=request, name="dashboard.html", context={"habits": habits}
        )


@app.post("/habits")
def create_habit(habit: HabitCreate):
    with DatabaseConnection(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO habits (name) VALUES (?)", (habit.name,))
        habit_id = cursor.lastrowid

    return {
        "message": f"a new habit {habit} is created",
        "habit_id": habit_id,
    }


@app.get("/habits")
def get_all_habits():
    with DatabaseConnection(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM habits")
        habits = cursor.fetchall()
    dict_habit = []
    for habit in habits:
        dict_habit.append({"id": habit["id"], "name": habit["name"]})
    return {"data": dict_habit}


@app.get("/habits/{name}")
def get_one_habit(name: str):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM habits WHERE name = (?)", (name,))
    habit = cursor.fetchone()

    conn.close()
    if habit is None:
        return "habit not found"
    return {"id": habit["id"], "name": habit["name"]}


@app.delete("/habits/{name}")
def delete_habit(name: str):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM habits WHERE name = ?", (name,))
    conn.commit()
    conn.close()
    return {"message": f"the habit {name} is deleted"}


@app.post("/logs/{habit_name_to_log}")
def log_habit(habit_name_to_log: str):
    with DatabaseConnection(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """SELECT id FROM habits WHERE name = (?)""", (habit_name_to_log,)
        )
        row = cursor.fetchone()
        if id is not None:
            today_date = str(date.today())
            cursor.execute(
                """INSERT INTO logs (habit_id, log_date)
                        VALUES (?,?)
                        """,
                (
                    row["id"],
                    today_date,
                ),
            )
            return {
                "message": f"the habit {habit_name_to_log} has been logged on {today_date}"
            }
        return {"message": "no logs found"}


@app.get("/logs/{habit}")
def get_logs(habit: str):
    with DatabaseConnection(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM habits WHERE name = (?)", (habit,))
        row = cursor.fetchone()
        cursor.execute("SELECT * FROM logs WHERE habit_id = (?)", (row["id"],))
        logs = cursor.fetchall()
    return {"data": logs}


@app.put("/habits/{name}")
def update_habit(update_name: HabitToUpdate):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE habits SET name = (?) WHERE name = (?)",
        (
            update_name.name_to_update_to,
            update_name.name,
        ),
    )
    conn.commit()
    conn.close()
    return {
        "message": f"the habit {update_name.name} has been changed to {update_name.name_to_update_to} "
    }
