import os
import sys
import sqlite3
import streamlit as st
from streamlit_cookies_controller import CookieController

cookies = CookieController()


def get_resource_path(filepath):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath("")

    resource_path = os.path.join(base_path, filepath)

    if os.path.exists(resource_path):
        return resource_path
    else:
        with open(resource_path, "w") as f:
            return resource_path


DATABASE_PATH = get_resource_path("data_files\\last_bite.db")

conn = sqlite3.connect(DATABASE_PATH)
cursor = conn.cursor()

# creating users table if not exists!
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
