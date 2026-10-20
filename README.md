# soccer-tactical-analyzer
# ⚽ Soccer Tactical & Match Analytics Engine

A Python-based web application that uses geometry and probability to analyze soccer tactics and predict match outcomes across Europe's top leagues.

### 🚀 Live App & Features
* **Live Web App:** [View the App Here](Insert-Your-Streamlit-URL-Here)
* **Dual-Team Formations:** Visualizes home and away team tactical shapes (like 3-2-4-1, 4-2-3-1, and 5-3-2) facing each other on a standard pitch.
* **Voronoi Spatial Control:** Splits the pitch into zones for each player to map out passing lanes and pressure areas.
* **Match Outcome Predictor:** Uses a Poisson probability model to calculate win/draw percentages and expected goals (xG) for any club matchup.
* **Database-Driven:** Pulls club ratings and formations dynamically from a multi-league CSV dataset.

### 🛠️ Tech Stack
* **Python**
* **Streamlit** (for the web interface)
* **Pandas & NumPy** (for data management and math)
* **Matplotlib & SciPy** (for pitch rendering and Voronoi geometry)

### 💻 How to Run Locally
1. Clone this repository.
2. Install dependencies:
   ```bash
   pip install streamlit pandas numpy matplotlib scipy
