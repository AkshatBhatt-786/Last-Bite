# Importing dependencies

import os
import sys
import sqlite3
import time
import re
import hashlib
from streamlit_cookies_controller import CookieController
from icecream import ic

ic.configureOutput(prefix="LastBite: ", includeContext=True)

def authenticate_email(email: str):
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(email_pattern, email))

def check_user_exists(email: str):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()
    return user[0] if user else None


def check_password_strength(password):
    password_pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[^a-zA-Z0-9]).{6,}$'
    return bool(re.match(password_pattern, password))


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def getResourcePath(filepath: str) -> str:
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    
    resource_path = os.path.join(base_path, filepath)
    
    if not os.path.exists(resource_path):
        ic(f"Setting up database at {resource_path}")
        os.makedirs(os.path.dirname(resource_path), exist_ok=True)  # ? Ensure directory exists
        with sqlite3.connect(resource_path) as conn:
            ic("Database initialized successfully.")
    else:
        ic(f"Database path configured at {resource_path}")
    
    return resource_path


# && Initialize DatabasePath
DATABASE_PATH = getResourcePath("data_files\\LastBite.db")


# && Initialize Cookies
cookies = CookieController()

conn = sqlite3.connect(DATABASE_PATH)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS inventory (
    item_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    item_name TEXT NOT NULL,
    quantity TEXT NOT NULL,
    unit TEXT NOT NULL,
    expiry_date TEXT NOT NULL,
    PRIMARY KEY (user_id, item_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
)
""")

conn.commit()
conn.close()
