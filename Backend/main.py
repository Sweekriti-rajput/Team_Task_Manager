from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3

app = FastAPI()

# Database connect
conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()

# Create tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT,
    password TEXT,
    role TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    status TEXT,
    assigned_to TEXT
)
""")

conn.commit()

# Models
class User(BaseModel):
    email: str
    password: str
    role: str

class Task(BaseModel):
    title: str
    status: str
    assigned_to: str

# APIs

@app.get("/")
def home():
    return {"message": "Backend running successfully"}

@app.post("/signup")
def signup(user: User):
    cursor.execute("INSERT INTO users (email, password, role) VALUES (?, ?, ?)",
                   (user.email, user.password, user.role))
    conn.commit()
    return {"message": "User created"}

@app.post("/login")
def login(user: User):
    cursor.execute("SELECT * FROM users WHERE email=? AND password=?",
                   (user.email, user.password))
    result = cursor.fetchone()
    if result:
        return {"message": "Login success", "role": result[3]}
    return {"message": "Invalid credentials"}

@app.post("/create-task")
def create_task(task: Task):
    cursor.execute("INSERT INTO tasks (title, status, assigned_to) VALUES (?, ?, ?)",
                   (task.title, task.status, task.assigned_to))
    conn.commit()
    return {"message": "Task created"}

@app.get("/tasks")
def get_tasks():
    cursor.execute("SELECT * FROM tasks")
    data = cursor.fetchall()
    return data

@app.put("/update-task/{task_id}")
def update_task(task_id: int, status: str):
    cursor.execute("UPDATE tasks SET status=? WHERE id=?", (status, task_id))
    conn.commit()
    return {"message": "Task updated"}
