import streamlit as st

with st.sidebar:

    st.header("Welcome to Last-Bite!")
    st.write("Reduce food waste by making the most of your ingredients.")

    st.page_link("pages/Home.py", label="Home", icon=":material/home:")
    st.page_link("pages/Inventory.py", label="Inventory", icon=":material/inventory:")
    st.page_link("pages/ViewRecipes.py", label="View Recipes", icon=":material/menu_book:")
