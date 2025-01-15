from database import cookies
import streamlit as st

if cookies.get("cookie_consent") == "accepted":
    st.session_state.logged_in = cookies.get("logged_in")
    st.session_state.user_email = cookies.get("user_email")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if st.session_state.logged_in:
    with st.sidebar:

        st.header(f"{st.session_state.user_email}\n, Welcome to Last-Bite!")
        st.write("Reduce food waste by making the most of your ingredients.")

        st.page_link("pages/Home.py", label="Home", icon=":material/home:")
        st.page_link("pages/Inventory.py", label="Inventory", icon=":material/inventory:")
        st.page_link("pages/ViewRecipes.py", label="View Recipes", icon=":material/menu_book:")
else:
    st.warning("You need to log in first to access this application.")
    st.write("Please visit the **Login Page** to proceed:")
    st.page_link("pages/Accounts.py", label="Go to Login Page", icon=":material/login:")
