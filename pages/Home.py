import streamlit as st

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if st.session_state.logged_in:
    with st.sidebar:

        st.header("Welcome to Last-Bite!")
        st.write("Reduce food waste by making the most of your ingredients.")

        st.page_link("pages/Home.py", label="Home", icon=":material/home:")
        st.page_link("pages/Inventory.py", label="Inventory", icon=":material/inventory:")
        st.page_link("pages/ViewRecipes.py", label="View Recipes", icon=":material/menu_book:")
else:
    from pages.Accounts import *
    login_tab, register_tab = st.tabs(["Login", "Register"])
    with login_tab:
        login_view()
    with register_tab:
        register_view()