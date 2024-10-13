import streamlit as st
import pandas as pd
from helpers.db_helpers import getconn

def show_rankings():
    st.title("Player Rankings :trophy:")

    # Establish database connection
    conn = getconn()

    # Query the player_rankings view
    query = "SELECT * FROM player_rankings ORDER BY player_rank"
    df = pd.read_sql(query, conn)

    # Close the connection
    conn.close()

    # Display the rankings
    st.dataframe(df.style.highlight_max(subset=["win%"], color='lightgreen'))

    # Additional statistics
    st.subheader("Top Players")
    top_players = df.head(3)
    for i, player in top_players.iterrows():
        st.markdown(f"{i+1}. Player {player['player_id']} - Win Rate: {player['win%']}%")

    # Overall statistics
    st.subheader("Overall Statistics")
    total_games = df['games_played'].sum()
    total_players = len(df)
    avg_win_rate = df['win%'].mean()

    st.metric("Total Games Played", total_games)
    st.metric("Total Players", total_players)
    st.metric("Average Win Rate", f"{avg_win_rate:.2f}%")