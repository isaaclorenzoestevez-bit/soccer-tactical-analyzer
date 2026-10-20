import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.spatial import Voronoi, voronoi_plot_2d
import streamlit as st

# Page Configuration
st.set_page_config(page_title="European Leagues Analytics Engine", layout="wide")
st.title("⚽ European Leagues Tactical & Match Analytics Engine")
st.write("Simulating dual-team tactical formations and match probabilities using current European club data.")

# 1. Load Data from CSV Database
@st.cache_data
def load_data():
    return pd.read_csv("european_teams.csv")

try:
    df_teams = load_data()
except FileNotFoundError:
    st.error("Error: 'european_teams.csv' not found on your Desktop! Please make sure both files are in the same folder.")
    st.stop()

# Pitch Dimensions
PITCH_LENGTH = 105.0
PITCH_WIDTH = 68.0

def draw_pitch(ax):
    ax.plot([0, 0, PITCH_LENGTH, PITCH_LENGTH, 0], [0, PITCH_WIDTH, PITCH_WIDTH, 0, 0], color="white", lw=2)
    ax.plot([PITCH_LENGTH / 2, PITCH_LENGTH / 2], [0, PITCH_WIDTH], color="white", lw=2)
    center_circle = plt.Circle((PITCH_LENGTH / 2, PITCH_WIDTH / 2), 9.15, color="white", fill=False, lw=2)
    ax.add_patch(center_circle)
    ax.set_facecolor("#2e8b57")
    ax.set_xlim(-5, PITCH_LENGTH + 5)
    ax.set_ylim(-5, PITCH_WIDTH + 5)
    ax.set_aspect("equal")
    ax.axis("off")

# Function to generate tactical coordinates based on formation string
def get_team_coordinates(formation_str, is_home=True):
    if formation_str == "3-2-4-1":
        coords = np.array([[15.0, 34.0], [30.0, 25.0], [30.0, 43.0], [45.0, 34.0], [55.0, 20.0], [55.0, 48.0], [70.0, 15.0], [70.0, 28.0], [70.0, 40.0], [70.0, 53.0], [88.0, 34.0]])
    elif formation_str == "5-3-2":
        coords = np.array([[20.0, 34.0], [35.0, 15.0], [35.0, 53.0], [45.0, 24.0], [45.0, 44.0], [60.0, 20.0], [60.0, 34.0], [60.0, 48.0], [75.0, 25.0], [75.0, 43.0], [85.0, 34.0]])
    elif formation_str == "3-4-2-1":
        coords = np.array([[18.0, 34.0], [32.0, 20.0], [32.0, 48.0], [48.0, 34.0], [58.0, 12.0], [58.0, 56.0], [68.0, 25.0], [68.0, 43.0], [78.0, 22.0], [78.0, 46.0], [86.0, 34.0]])
    elif formation_str == "4-4-2":
        coords = np.array([[15.0, 34.0], [30.0, 18.0], [30.0, 50.0], [45.0, 34.0], [55.0, 15.0], [55.0, 30.0], [55.0, 38.0], [55.0, 53.0], [75.0, 25.0], [75.0, 43.0], [85.0, 34.0]])
    else:  # Default 4-3-3
        coords = np.array([[15.0, 34.0], [30.0, 22.0], [30.0, 46.0], [45.0, 34.0], [58.0, 20.0], [58.0, 48.0], [70.0, 15.0], [70.0, 34.0], [70.0, 53.0], [82.0, 28.0], [85.0, 34.0]])
    
    # If away team, mirror coordinates across the centerline so they face right-to-left
    if not is_home:
        coords[:, 0] = PITCH_LENGTH - coords[:, 0]
        
    return coords

# 2. Sidebar League & Matchup Selectors
st.sidebar.header("🇪🇺 League & Matchup Simulator")
selected_league = st.sidebar.selectbox("Select League", df_teams["League"].unique())
league_teams = df_teams[df_teams["League"] == selected_league]["Team"].tolist()

team_a_name = st.sidebar.selectbox("Home Team (Team A)", league_teams, index=0)
team_b_name = st.sidebar.selectbox("Away Team (Team B)", league_teams, index=1 if len(league_teams) > 1 else 0)

# Fetch club details from CSV
row_a = df_teams[df_teams["Team"] == team_a_name].iloc[0]
row_b = df_teams[df_teams["Team"] == team_b_name].iloc[0]

form_a = str(row_a["Formation"]) if "Formation" in df_teams.columns else "4-3-3"
form_b = str(row_b["Formation"]) if "Formation" in df_teams.columns else "4-3-3"

st.sidebar.markdown(f"**{team_a_name} Formation:** `{form_a}`")
st.sidebar.markdown(f"**{team_b_name} Formation:** `{form_b}`")

st.sidebar.header("Ball Positioning")
ball_x = st.sidebar.slider("Ball X Coordinate", 10.0, 95.0, 52.5)
ball_y = st.sidebar.slider("Ball Y Coordinate", 5.0, 63.0, 34.0)

# 3. Generate Dual-Team Formations & Voronoi Geometry
team_a_players = get_team_coordinates(form_a, is_home=True)
team_b_players = get_team_coordinates(form_b, is_home=False)

all_players = np.vstack([team_a_players, team_b_players])
vor = Voronoi(all_players)

fig, ax = plt.subplots(figsize=(10, 6))
draw_pitch(ax)
voronoi_plot_2d(vor, ax=ax, show_vertices=False, line_colors="yellow", line_width=1.5, line_style="--")

ax.scatter(team_a_players[:, 0], team_a_players[:, 1], color="blue", s=150, label=f"{team_a_name} ({form_a})", zorder=5)
ax.scatter(team_b_players[:, 0], team_b_players[:, 1], color="red", s=150, label=f"{team_b_name} ({form_b})", zorder=5)
ax.scatter(ball_x, ball_y, color="black", s=100, marker="o", label="Ball Position", zorder=6)
ax.legend(loc="upper left")
st.pyplot(fig)

# 4. Pure Python Poisson Distribution Match Prediction Model
def poisson_pmf(k, lam):
    return (math.exp(-lam) * (lam ** k)) / math.factorial(k)

lambda_a = row_a["AttackRating"] * row_b["DefenseRating"] * 0.9
lambda_b = row_b["AttackRating"] * row_a["DefenseRating"] * 0.85

max_goals = 6
prob_matrix = np.zeros((max_goals, max_goals))
for i in range(max_goals):
    for j in range(max_goals):
        prob_matrix[i, j] = poisson_pmf(i, lambda_a) * poisson_pmf(j, lambda_b)

home_win = np.sum(np.tril(prob_matrix, -1))
draw = np.sum(np.diag(prob_matrix))
away_win = np.sum(np.triu(prob_matrix, 1))

st.write(f"### 📊 Match Outcome Probabilities: {team_a_name} vs {team_b_name}")
col1, col2, col3 = st.columns(3)
col1.metric(f"{team_a_name} Win", f"{home_win*100:.1f}%")
col2.metric("Draw", f"{draw*100:.1f}%")
col3.metric(f"{team_b_name} Win", f"{away_win*100:.1f}%")
st.info(f"**Expected Goals (xG) Model:** {team_a_name} ({lambda_a:.2f}) - ({lambda_b:.2f}) {team_b_name}")