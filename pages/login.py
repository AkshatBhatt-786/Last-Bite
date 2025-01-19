# Importing dependencies

from initalizer import *
import streamlit as st

# ^ settings ^
try:
    st.set_page_config(page_title="Login | LastBite", page_icon="🍪", layout="centered")
except Exception as e:
    pass


# ^ utilities ^

def on_login(email: str, password: str) -> None:
    if email == "" and password == "":
        st.warning("All fields are required!")
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
            cookies.set("logged_in", True)
            cookies.set("user_email", email)
            return True
        else:
            st.error("Invalid email or password.")
            return False
    else:
        st.error("Invalid email or password.")
        return False


# ^ cookies & sessions ^

# Check if the "logged_in" session state variable is initialized. //
# If not, initialize it to False and log the default state. //

if cookies.get("cookie_consent"):
    st.session_state.logged_in = cookies.get("logged_in")
    st.session_state.user_email = cookies.get("user_email")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    ic(f"[Session State] Initialized 'logged_in' to {st.session_state.logged_in}")

# Check if the "user_email" session state variable is initialized. //
# If not, initialize it to an empty string and log the default state. //
if "user_email" not in st.session_state:
    st.session_state.user_email = ""
    ic(f"[Session State] Initialized 'user_email' to an empty string")

if "user_password" not in st.session_state:
    st.session_state.user_password = ""

if "current_page" not in st.session_state:
    st.session_state.current_page = "login_page"
    ic(f"[Session State] page : Login")

if st.session_state.logged_in:
    st.session_state.current_page = "home_page"
    st.switch_page("pages/home.py")


# ^ App UI ^

with st.form("login-form"):
    st.header(":blue[_Welcome Back_!] :smile:")

    st.subheader("Log in to Last Bite and continue your culinary journey.", anchor="left", divider=True)
    email = st.text_input("Email", placeholder="enter your email address", value=st.session_state.get("user_email", ""))
    password = st.text_input("Password", placeholder="******", value=st.session_state.get("user_password", ""), type="password")

    login_btn = st.form_submit_button("LOGIN", icon=":material/login:")
    if login_btn:
        auth_user = on_login(email, password)
        if auth_user:
            st.session_state.logged_in = True
            st.session_state.user_email = email
            st.toast(f"Successfully logged in as {email}")
            st.rerun()
    st.markdown("Don't have an account ? [click here](register)")

