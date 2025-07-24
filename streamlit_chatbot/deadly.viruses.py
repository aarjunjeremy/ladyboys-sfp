import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# -------------------- PAGE CONFIG --------------------
st.set_page_config(page_title="GRAPH OF DIFFERENT PANDEMIC", page_icon="🦠", layout="wide")

st.title("📊 GRAPH OF DIFFERENT PANDEMIC (MEGA VERSION)")

# -------------------- SIDEBAR --------------------
pandemics = [
    "COVID-19",
    "AIDS",
    "The Third Plague",
    "1918 Flu"
]

if "confirmed" not in st.session_state:
    st.session_state.confirmed = False

with st.sidebar:
    pandemic = st.selectbox("Select Pandemic", pandemics)

    if pandemic == "COVID-19":
        year_range = list(range(2019, 2025))
    elif pandemic == "AIDS":
        year_range = list(range(1980, 2025))
    elif pandemic == "The Third Plague":
        year_range = list(range(1855, 1959))
    elif pandemic == "1918 Flu":
        year_range = list(range(1918, 1921))

    year = st.selectbox("Select Year", year_range)
    month = st.slider("Select Month", 1, 12)

    mode = st.radio("Background Mode", ["Light", "Dark"])

    if st.button("✅ Confirm Selection"):
        st.session_state.pandemic = pandemic
        st.session_state.year = year
        st.session_state.month = month
        st.session_state.mode = mode
        st.session_state.confirmed = True

# -------------------- BACKGROUND --------------------
if st.session_state.get("mode", "Light") == "Light":
    bg_image = "https://images.unsplash.com/photo-1614763875780-90481c10a1ba?ixlib=rb-4.0.3&auto=format&fit=crop&w=1470&q=80"
else:
    bg_image = "https://images.unsplash.com/photo-1583766395091-c204d7d8ec3c?ixlib=rb-4.0.3&auto=format&fit=crop&w=1470&q=80"

st.markdown(
    f"""
    <style>
    body {{
        background: url('{bg_image}') no-repeat center center fixed;
        background-size: cover;
    }}
    .main {{
        background-color: rgba(0,0,0,0.5);
        padding: 2rem;
        border-radius: 1rem;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# -------------------- BACKGROUND MUSIC --------------------
st.markdown(
    """
    <audio id="bg-music" loop>
      <source src="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3" type="audio/mpeg">
    </audio>
    <button onclick="document.getElementById('bg-music').play()">▶️ Play Music</button>
    """,
    unsafe_allow_html=True
)

# -------------------- GENERATE PANDEMIC DATA --------------------
def get_pandemic_data(pandemic, year):
    np.random.seed(year)  # so it's consistent for same year
    months = pd.date_range(start=f"{year}-01-01", end=f"{year}-12-31", freq='M')

    if pandemic == "COVID-19":
        base = np.abs(np.sin(np.linspace(0, 3 * np.pi, len(months)))) * 150000
    elif pandemic == "AIDS":
        base = np.linspace(1000, 100000, len(months)) + np.random.normal(0, 2000, len(months))
    elif pandemic == "The Third Plague":
        base = np.abs(np.sin(np.linspace(0, 2 * np.pi, len(months)))) * 40000 + 8000
    elif pandemic == "1918 Flu":
        base = np.exp(-0.5 * ((np.linspace(-1, 1, len(months))) ** 2)) * 120000 + np.random.normal(0, 2000, len(months))
    else:
        base = np.zeros(len(months))

    base = np.maximum(base, 0)
    return pd.DataFrame({"Month": months, "Cases": base.astype(int)})

# -------------------- DISPLAY CHART --------------------
if st.session_state.confirmed:
    df = get_pandemic_data(st.session_state.pandemic, st.session_state.year)
    selected_month = df[df["Month"].dt.month == st.session_state.month]

    fig = px.line(
        df,
        x="Month",
        y="Cases",
        title=f"{st.session_state.pandemic} Cases in {st.session_state.year}"
    )

    fig.add_scatter(
        x=selected_month["Month"],
        y=selected_month["Cases"],
        mode="markers+text",
        text=selected_month["Cases"],
        textposition="top center",
        marker=dict(size=10, color="red"),
        name="Selected Month"
    )

    st.plotly_chart(fig, use_container_width=True)
    st.success(f"Showing **{st.session_state.pandemic}**, Year: **{st.session_state.year}**, Month: **{st.session_state.month}**")
else:
    st.info("Please select your options in the sidebar and click **✅ Confirm Selection** to view the graph.")
