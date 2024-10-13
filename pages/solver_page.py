import streamlit as st
from solver.connect_four_solver import solve_connect_four
from helpers.streamlit_helpers import (
    display_result,
    save_uploaded_file
)
from helpers.db_helpers import write_to_database
import os


def show_solver_page():
    st.title("Connect Four Solver")

    uploaded_file = st.file_uploader("Choose a file", type="txt")
    if uploaded_file is not None:
        # Display the contents of the uploaded file
        content = uploaded_file.getvalue().decode("utf-8")
        st.write("Uploaded Connect Four board:")
        st.text(content)
        
        if st.button("Solve and save results to db"):
            try:
                # Save the uploaded file to a temporary file
                temp_file_path = save_uploaded_file(uploaded_file)
                
                # Call the solver with the temporary file path
                result = solve_connect_four(temp_file_path)
                display_result(result)
                if write_to_database(result):
                    st.success("Results saved to database!")

                
                # Clean up the temporary file
                os.unlink(temp_file_path)
            except Exception as e:
                st.error(f"An error occurred while solving: {str(e)}")