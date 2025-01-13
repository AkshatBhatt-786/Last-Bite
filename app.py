# dependencies

import os
import sys
from database import *
import streamlit as st

st.set_page_config(page_title="Get Started with Last-Bite")

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
    st.title("Welcome to Last-Bite!")
    st.subheader("Transform Your Leftovers into Delicious Meals and Reduce Food Waste!")
    st.write("""
    Last-Bite is an innovative app designed to help you make the most of your ingredients and reduce food waste. 
    Join us in the fight against waste by turning what you have into something delicious!
    """)

    # Key Features
    st.header("Key Features")
    st.write("""
    - **Recipe Suggestions**: Enter the ingredients you have, and get creative recipes tailored to reduce waste.
    - **Expiration Reminders**: Receive notifications for ingredients nearing their expiration dates, so you can use them in time.
    - **Community Sharing**: Share your favorite recipes and tips with a community of like-minded individuals.
    - **Sustainability Tips**: Learn practical tips on how to reduce waste in your kitchen and make a positive impact on the environment.
    """)

    # Call to Action Section
    st.header("Get Started Today!")
    st.write("""
    Create an account or log in to access all features and start your journey towards reducing food waste.
    """)
    st.page_link("pages/Accounts.py", label="Get Started!", icon=":material/call_to_action:")


    # About Us Section
    st.header("About Us")
    st.write("""
    At Last-Bite, we believe that every ingredient has the potential to create something wonderful. 
    Our mission is to empower individuals to reduce food waste and make sustainable choices in their kitchens.
    """)

    # Contact Information
    st.header("Contact Us")
    st.write("""
    For inquiries, feedback, or support, feel free to reach out to us at: 
    **support@lastbiteapp.com**
    """)

    with st.sidebar:
        st.header("Welcome to Last-Bite!")
        st.sidebar.subheader("Reduce Food Waste")
        st.sidebar.write(
            "Join us in the fight against food waste by making the most of your ingredients. Last-Bite helps you transform leftovers into delicious meals!")
        st.markdown("---")
        st.sidebar.header("Features")
        st.sidebar.write("- **Recipe Suggestions**: Get creative recipes based on the ingredients you have.")
        st.sidebar.write("- **Expiration Reminders**: Never let food go to waste with timely reminders.")
        st.sidebar.write("- **Community Sharing**: Share your recipes and tips with others.")
        st.sidebar.write("- **Sustainability Tips**: Learn how to reduce waste in your kitchen.")

