import os
import streamlit as st

from pages.rankings_page import show_rankings
from pages.solver_page import show_solver_page



st.set_page_config(
    page_title="",  # This removes the title from the sidebar
    initial_sidebar_state="expanded"
)

hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

def main():

    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Solve Connect Four", "Player Rankings"])
    
    if page == "Solve Connect Four":
        show_solver_page()
    elif page == "Player Rankings":
        show_rankings()

    st.sidebar.header("About")
    st.sidebar.info("Hello! This app uses a Connect Four solver to analyze game states from text file input.")

if __name__ == "__main__":
    main()