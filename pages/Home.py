# Importing dependencies
from initalizer import *
import streamlit as st

# ^ settings ^
try:
    st.set_page_config(page_title="Home | LastBite", page_icon="🍪", layout="centered")
except Exception as e:
    pass


# ^ cookies & sessions ^


if cookies.get("cookie_consent"):
    st.session_state.logged_in = cookies.get("logged_in")
    st.session_state.user_email = cookies.get("user_email")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    ic(f"[Session State] Initialized 'logged_in' to {st.session_state.logged_in}")
    time.sleep(2)
    st.switch_page("pages/login.py")

if "user_email" not in st.session_state:
    st.session_state.user_email = ""
    ic(f"[Session State] Initialized 'user_email' to an empty string")


if "current_page" not in st.session_state:
    st.session_state.current_page = "home_page"
    ic(f"[Session State] page : Home")

if st.session_state.logged_in:
    st.session_state.current_page = "home_page"
    with st.sidebar:
        st.header("🍪 Last-Bite Menu")
        st.write(f"Welcome back, **{st.session_state.user_email}**!")
        st.divider()

        # Navigation links
        st.markdown("### 📂 Navigation")
        st.page_link("pages/inventory.py", label="Inventory", icon=":material/inventory:")
        st.page_link("pages/recipes.py", label="Recipes", icon=":material/menu_book:")

        st.divider()

        # User account management
        st.markdown(":material/account_circle: ###Account")
        if st.button("Log Out", key="logout"):
            st.session_state.logged_in = False
            cookies.remove("logged_in")
            cookies.remove("user_email")
            st.toast("You have been logged out successfully!")
            time.sleep(2)
            st.switch_page("pages/login.py")

        st.divider()

        # Contact/Support info
        st.markdown("### 📧 Need Help?")
        st.write("[Contact Us](mailto:LastBite.support@gmail.com)")

    # ^ Main Content: Home Page ^

    st.title("🍪 Welcome to Last-Bite!")
    st.write("Your one-stop platform for reducing food waste, saving money, and planning delicious meals!")

    st.divider()

    # Key Features Section
    st.markdown("""
    ### 🌟 Key Features:
    1. **Smart Inventory Management**: Track your pantry, fridge, and freezer items with ease.
    2. **Personalized Recipe Suggestions**: Get creative recipes based on what you already have at home.
    3. **Meal Planner**: Organize your week with meal plans tailored to your preferences and available ingredients.
    4. **Food Waste Insights**: Monitor how much food you’re saving and reduce your environmental impact.
    """)

    st.divider()

    # Call-to-Action Buttons
    col1, col2, col3 = st.columns(3, gap="large")
    with col1:
        if st.button("Manage Inventory", key="cta-inventory"):
            st.switch_page("pages/inventory.py")
    with col2:
        if st.button("Get Recipes", key="cta-recipes"):
            st.switch_page("pages/recipes.py")
    with col3:
        if st.button("Plan Meals", key="cta-meal-planner"):
            st.switch_page("pages/meal_planner.py")

    st.divider()

    # Footer
    st.markdown("""
    _Last-Bite: Making every bite count!_
    """)
else:
    st.switch_page("pages/home.py")