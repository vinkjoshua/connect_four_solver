import streamlit as st
import tempfile

def display_result(result):
    st.subheader("Solver Results")
    for i, game_result in enumerate(result, 1):
        with st.expander(f"Game {i} Result", expanded=True):
            if "won" in game_result:
                winner, moves = game_result.split(" won in ")
                st.markdown(f"**Winner:** :trophy: {winner}")
                st.markdown(f"**Moves:** :arrows_counterclockwise: {moves}")
            elif "Draw" in game_result:
                players = game_result.split("Draw between ")[1]
                st.markdown(f"**Result:** :handshake: Draw")
                st.markdown(f"**Players:** {players}")
            else:
                st.write(game_result) 


def save_uploaded_file(uploaded_file):
    # Create a temporary file
    with tempfile.NamedTemporaryFile(delete=False, mode='w+', suffix='.txt') as tmp_file:
        # Write the contents of the uploaded file to the temporary file
        tmp_file.write(uploaded_file.getvalue().decode("utf-8"))
        # Return the path of the temporary file
        return tmp_file.name