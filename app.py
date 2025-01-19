# Importing dependencies

from initalizer import *
import streamlit as st

# ^ settings ^
try:
    st.set_page_config(page_title="Get Started with Last-Bite", page_icon="🍪", layout="centered")
except Exception as e:
    pass


# ^ cookies & sessions ^

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
    st.session_state.current_page = "landing_page"
    ic(f"[Session State] page : Landing")


# Dialog function to ask for cookie consent
@st.dialog(title="Accept Cookies", width="small")
def askCookies():
    """
    Displays a dialog to request cookie consent from the user.
    If the user accepts or declines, it updates the cookies and refreshes the page.
    """

    st.write("We use cookies to improve your experience. By clicking 'Accept', you agree to our cookie policy.")
    col1, col2 = st.columns(2, vertical_alignment="center", gap="large")
    with col1:
        accept_cookies_btn = st.button(
            "Accept Cookies",
            icon=":material/cookie:",
            key="accept_cookies_btn",
            type="secondary"
        )
        if accept_cookies_btn:
            cookies.set("cookie_consent", True, max_age=86400)
            st.rerun()

    with col2:
        decline_cookies_btn = st.button(
            "Decline Cookies",
            key="decline_cookies_btn",
            icon=":material/cookie_off:",
            type="primary"
        )
        if decline_cookies_btn:
            cookies.set("cookie_consent", False, max_age=86400)
            st.rerun()
            
# Check for cookie consent and display dialog if needed
if cookies.get("cookie_consent") is None:
    askCookies()
    
if not cookies.get("cookie_consent"):
    st.warning("You have declined cookies. Some features may not work.")

# ^ App UI ^

if st.session_state.current_page == "landing_page":
    if not st.session_state.logged_in:
        with st.sidebar:
            st.markdown("## 🍪 Welcome to Last-Bite!")
            st.write("Join us to start saving food, reducing waste, and discovering amazing recipes.")
    
            col1, col2 = st.columns(2, gap="small", vertical_alignment="top")
            with col1:
                if st.button("Sign In", key="redirect-login"):
                    st.switch_page("pages/login.py")
            with col2:
                if st.button("Sign Up", key="redirect-register"):
                    st.switch_page("pages/register.py")
    
            st.divider()
    
        
            st.markdown("### Why Join Us?")
            st.markdown("""
            - 🥗 **Discover Recipes**: Make the most of your ingredients.
            - 🛒 **Plan Your Meals**: Save money and reduce waste.
            - 🌍 **Track Your Impact**: See how much food you save.
            """)
    
            st.divider()
            # Contact/Support info
            st.markdown("### Need Help?")
            st.write("📧 [Contact Us](mailto:LastBite.support@gmail.com)")
    
    st.title("🍪 Welcome to Last-Bite!")
    st.write("A platform dedicated to helping you **reduce food waste** and make the most of your kitchen ingredients. Let’s work together to save food, save money, and save the planet!")
    st.divider()
    st.markdown("""
    ### Your Ultimate Food Companion
    Discover recipes, track your meals, and make every bite count with **Last-Bite**. Get started now!
    """)
    st.markdown("""
    #### 🌟 **Features You'll Love**  
    - **Smart Inventory Management**: Track your pantry, fridge, and freezer items with ease. (click here)[Inventory]
    - **Personalized Recipe Suggestions**: Get creative recipes based on what you already have at home.  
    - **Plan Your Meals**: Organize your week with meal plans tailored to your preferences and available ingredients.  
    - **Food Waste Insights**: Monitor how much food you’re saving and reduce your environmental impact.  
    """)
    