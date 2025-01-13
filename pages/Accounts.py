import time
from database import DATABASE_PATH, cookies
import sqlite3
import re
import hashlib
import streamlit as st


@st.dialog("Accept Cookies", width="small")
def ask_cookies():
    st.write("We use cookies to improve your experience. By clicking 'Accept', you agree to our cookie policy.")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Accept Cookies"):
            cookies.set("cookie_consent", "accepted", max_age=86400)
            st.rerun()
    with col2:
        if st.button("Decline Cookies"):
            cookies.set("cookie_consent", "declined", max_age=86400)
            st.rerun()


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_email" not in st.session_state:
    st.session_state.user_email = ""


def check_user_exists(email: str):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()
    return user[0] if user else None


def authenticate_email(email: str):
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(email_pattern, email))


def register_new_user(email, password):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    hashed_password = hash_password(password)

    try:
        cursor.execute("""
        INSERT INTO users (email, password, created_at)
        VALUES (?, ?, CURRENT_TIMESTAMP);
        """, (email, hashed_password))
        conn.commit()
        st.success(f"{email} account created successfully!")

    except sqlite3.IntegrityError as e:
        ic(f"Error: {e}")

    finally:
        conn.close()


def check_password_strength(password):
    password_pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[^a-zA-Z0-9]).{6,}$'
    return bool(re.match(password_pattern, password))


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def on_register(email: str, password: str):
    formatted_email = authenticate_email(email)
    if not formatted_email:
        st.error(f"The given email {email} isn't valid!")
        return False

    user = check_user_exists(email)
    if user:
        st.error(f"{email} already exists!")
        time.sleep(2)
        return False

    strong_valid_password = check_password_strength(password)
    if not strong_valid_password:
        st.error("""
            Validates a password based on the following criteria:
            - At least 6 characters long.
            - Contains at least one lowercase letter.
            - Contains at least one uppercase letter.
            - Contains at least one symbol (non-alphanumeric character).
                """)
        return False

    register_new_user(email, password)
    time.sleep(2)
    return True



def on_login(email: str, password: str) -> bool:
    if email == "" and password == "":
        st.error("All fields are required!")
        return False
    users = check_user_exists(email)
    if users is None:
        st.error("Invalid username or password.")
        time.sleep(2)
        return False

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, email, password FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()
    if user:
        stored_password = user[2]
        if stored_password == hash_password(password):
            return True
        else:
            st.error("Invalid email or password.")
            return False
    else:
        st.error("Invalid email or password.")
        return False


def login_view():
    with st.form("Login-Form"):
        st.header("Welcome Back!")
        st.subheader("Log in to Last Bite and continue your culinary journey.")
        st.markdown("---")

        # Input fields
        user_email = st.text_input(
            "Email Address",
            value=st.session_state.get("user_email", ""),
            placeholder="Enter your email address"
        )
        user_password = st.text_input(
            "Password",
            value=st.session_state.get("user_password", ""),
            placeholder="Enter your password",
            type="password"
        )

        # Submit button
        if st.form_submit_button("Log In"):
            auth_user = on_login(user_email, user_password)
            if auth_user:
                st.session_state.logged_in = True
                st.session_state.user_email = user_email
                st.rerun()


def register_view():
    with st.form("Register-Form"):
        st.header("Create Your Account")
        st.subheader("Join Last Bite and savor every moment!")

        # Input fields
        register_email = st.text_input("Email Address", value=st.session_state.get("register_email", ""), placeholder="Enter your email address")
        register_password = st.text_input("Create Password", value=st.session_state.get("register_password", ""), placeholder="Choose a strong password", type="password")

        # Submit button
        if st.form_submit_button("Register Now"):
            register_user = on_register(register_email, register_password)
            if register_user:
                st.session_state.logged_in = True
                st.session_state.user_email = register_email
                st.rerun()


def handle_cookie_consent():
    if cookies.get("cookie_consent") is None:
        ask_cookies()
    elif cookies.get("cookie_consent") == "declined":
        st.warning("You have declined cookies. Some features may not work.")


if st.session_state.logged_in:
    from pages.Home import *
else:
    handle_cookie_consent()
    login_tab, register_tab = st.tabs(["Login", "Register"])
    with login_tab:
        login_view()
    with register_tab:
        register_view()

