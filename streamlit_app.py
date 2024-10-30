import streamlit as st
import pandas as pd
from nba_api.stats.endpoints import leaguedashplayerstats, leaguedashteamstats
import altair as alt

# Set Streamlit page configuration
st.set_page_config(page_title="Enhanced NBA Stats Comparison", layout="wide")

# Function to get team stats
@st.cache_data
def get_team_stats(per_mode="PerGame"):
    team_stats = leaguedashteamstats.LeagueDashTeamStats(
        season='2024-25',
        season_type_all_star='Regular Season',
        per_mode_detailed=per_mode
    )
    return team_stats.get_data_frames()[0]

# Function to get player stats
@st.cache_data
def get_player_stats(per_mode="PerGame"):
    player_stats = leaguedashplayerstats.LeagueDashPlayerStats(
        season='2024-25',
        season_type_all_star='Regular Season',
        per_mode_detailed=per_mode
    )
    return player_stats.get_data_frames()[0]

# Sidebar options
st.sidebar.title("NBA Stats Comparison")
comparison_type = st.sidebar.selectbox("Choose Comparison Type", ["Team", "Player"])
per_mode = st.sidebar.radio("Stats Type", ["PerGame", "Totals"])

# Team comparison setup
if comparison_type == "Team":
    st.header("Enhanced Team Stats Comparison")
    team_stats = get_team_stats(per_mode)
    team1 = st.selectbox("Select Team 1", team_stats["TEAM_NAME"].unique())
    team2 = st.selectbox("Select Team 2", team_stats["TEAM_NAME"].unique())
    team1_stats = team_stats[team_stats["TEAM_NAME"] == team1]
    team2_stats = team_stats[team_stats["TEAM_NAME"] == team2]
    
    # Display key stats
    selected_stats = ["FG_PCT", "REB", "AST", "TOV", "PTS"]
    team1_filtered = team1_stats[selected_stats].T.rename(columns={team1_stats.index[0]: team1})
    team2_filtered = team2_stats[selected_stats].T.rename(columns={team2_stats.index[0]: team2})

    st.subheader(f"Comparing {team1} and {team2} Key Stats")
    st.write("### Key Stats for Both Teams")
    st.write(pd.concat([team1_filtered, team2_filtered], axis=1))

    # Interactive Chart
    st.write("### Team Stats Comparison Chart")
    chart_data = pd.concat([team1_filtered, team2_filtered], axis=1).reset_index().melt("index")
    chart = alt.Chart(chart_data).mark_bar().encode(
        x="index:N",
        y="value:Q",
        color="variable:N",
        tooltip=["index", "value"]
    ).properties(width=600)
    st.altair_chart(chart)

# Player comparison setup
elif comparison_type == "Player":
    st.header("Enhanced Player Stats Comparison")
    player_stats = get_player_stats(per_mode)
    player1 = st.selectbox("Select Player 1", player_stats["PLAYER_NAME"].unique())
    player2 = st.selectbox("Select Player 2", player_stats["PLAYER_NAME"].unique())
    player1_stats = player_stats[player_stats["PLAYER_NAME"] == player1]
    player2_stats = player_stats[player_stats["PLAYER_NAME"] == player2]
    
    # Display key stats
    selected_stats = ["FG_PCT", "REB", "AST", "TOV", "PTS"]
    player1_filtered = player1_stats[selected_stats].T.rename(columns={player1_stats.index[0]: player1})
    player2_filtered = player2_stats[selected_stats].T.rename(columns={player2_stats.index[0]: player2})

    st.subheader(f"Comparing {player1} and {player2} Key Stats")
    st.write("### Key Stats for Both Players")
    st.write(pd.concat([player1_filtered, player2_filtered], axis=1))

    # Interactive Chart
    st.write("### Player Stats Comparison Chart")
    chart_data = pd.concat([player1_filtered, player2_filtered], axis=1).reset_index().melt("index")
    chart = alt.Chart(chart_data).mark_bar().encode(
        x="index:N",
        y="value:Q",
        color="variable:N",
        tooltip=["index", "value"]
    ).properties(width=600)
    st.altair_chart(chart)
    st.write("### Player 1 Stats")
    st.write(player1_stats)
    st.write("### Player 2 Stats")
    st.write(player2_stats)
