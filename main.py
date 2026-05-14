import sqlite3

from fastapi import FastAPI
from pydantic import BaseModel

DATABASE = "data.db"


class HabitCreate(BaseModel):
    name: str
    logs: str


class HabitToUpdate(BaseModel):
    name: str
    name_to_update_to: str


def create_table():
    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS habits   (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    logs TEXT           
               )
               """)

    conn.commit()
    conn.close()


create_table()
app = FastAPI()


@app.get("/")
def home():
    return {"message": "the table has been created and running"}


@app.post("/habits")
def create_habit(habit: HabitCreate):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO habits (name) VALUES (?)", (habit.name,))
    conn.commit()
    habit_id = cursor.lastrowid
    conn.close()

    return {
        "message": f"a new habit {habit} is created",
        "habit_id": habit_id,
    }


@app.get("/habits")
def get_all_habits():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM habits")
    habits = cursor.fetchall()
    conn.close()
    dict_habit = []
    for habit in habits:
        dict_habit.append({"id": habit[0], "name": habit[1]})
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
    return {"id": habit[0], "name": habit[1]}


@app.delete("/habits/{name}")
def delete_habit(name: str):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM habits WHERE name = ?", (name,))
    conn.commit()
    conn.close()
    return {"message": f"the habit {name} is deleted"}


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
