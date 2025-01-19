# Importing dependencies

from initalizer import *
import streamlit as st


# ^ settings ^
try:
    st.set_page_config(page_title="Register | LastBite", page_icon="🍪", layout="centered")
except Exception as e:
    pass


# ^ utilities ^

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


def on_register(email: str, password: str):
    ic(email, password)
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
    st.session_state.logged_in = True
    st.session_state.user_email = register_email
    register_new_user(email, password)
    st.toast(f"successfully logged in as {email}")
    time.sleep(2)
    st.switch_page("pages/home.py")
    return True


# ^ cookies & sessions ^

if cookies.get("cookie_consent"):
    st.session_state.logged_in = cookies.get("logged_in")
    st.session_state.user_email = cookies.get("user_email")

# Check if the "logged_in" session state variable is initialized. 
# If not, initialize it to False and log the default state. 
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    ic(f"[Session State] Initialized 'logged_in' to {st.session_state.logged_in}")

# Check if the "user_email" session state variable is initialized. 
# If not, initialize it to an empty string and log the default state. 
if "user_email" not in st.session_state:
    st.session_state.user_email = ""
    ic(f"[Session State] Initialized 'user_email' to an empty string")

if "current_page" not in st.session_state:
    st.session_state.current_page = "register_page"
    ic(f"[Session State] page : Register")



# ^ App UI ^

if st.session_state.logged_in:
    st.session_state.current_page = "home_page"
    ic(f"[Session State] page : Home")
    st.switch_page("pages/home.py")
else:
    with st.form("register-form"):
        st.header(":blue[Create Your Account] :sunglasses:")

        st.subheader("Join Last Bite and savor every moment!", anchor="left", divider=True)
        register_email = st.text_input("Email", placeholder="enter your email address")
        register_password = st.text_input("Password", placeholder="Create Strong Password", type="password")

        register_btn = st.form_submit_button("REGISTER", icon=":material/login:")
        if register_btn:
            register_user = on_register(register_email, register_password)
            if register_user:
                st.session_state.logged_in = True
                st.session_state.user_email = register_email

        st.markdown("Already have an account ? [click here](login)")