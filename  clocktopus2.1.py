import streamlit as st
from streamlit_folium import st_folium
import folium
from folium.features import DivIcon
import datetime
import pytz
import time

# -------------------- Custom CSS for animated octopus and background --------------------
st.markdown(
    """
    <style>
    body {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    }
    .main {
        background-color: rgba(0, 0, 0, 0.5);
        padding: 2rem;
        border-radius: 1rem;
    }
    .rotate {
        animation: rotation 4s infinite linear;
    }
    @keyframes rotation {
        from {
            transform: rotate(0deg);
        }
        to {
            transform: rotate(359deg);
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -------------------- Cities --------------------
cities = {
    "Kuala Lumpur": (3.1390, 101.6869, "Asia/Kuala_Lumpur", "Rainy, 28°C", "Hari Raya Celebration"),
    "New York": (40.7128, -74.0060, "America/New_York", "Cloudy, 18°C", "NYC Marathon"),
    "London": (51.5074, -0.1278, "Europe/London", "Sunny, 22°C", "Royal Parade"),
    "Tokyo": (35.6895, 139.6917, "Asia/Tokyo", "Clear, 25°C", "Tokyo Summer Fest"),
    "Sydney": (-33.8688, 151.2093, "Australia/Sydney", "Windy, 15°C", "Sydney Vivid Lights"),
    "Singapore": (1.3521, 103.8198, "Asia/Singapore", "Humid, 30°C", "National Day Prep"),
}

# -------------------- Page config --------------------
st.set_page_config(page_title="Clocktopus", page_icon="🐙", layout="wide")
st.title("🐙 Clocktopus")
st.header("Time Zones in Every Tentacle!")

# -------------------- Tabs --------------------
tabs = st.tabs(["🌍 Map", "⏰ Alarm", "⏱️ Stopwatch", "⏳ Timer"])

# -------------------- Theme switcher --------------------
theme = st.sidebar.radio("Map Theme", options=["Dark", "Light", "Satellite"])
if theme == "Dark":
    tiles = "CartoDB dark_matter"
elif theme == "Light":
    tiles = "OpenStreetMap"
else:
    tiles = "Stamen Terrain"

# -------------------- Malaysia Time Snapshot --------------------
malaysia_tz = pytz.timezone("Asia/Kuala_Lumpur")
if "snapshot" not in st.session_state:
    st.session_state.snapshot = datetime.datetime.now(malaysia_tz)
snapshot = st.session_state.snapshot

# -------------------- Map tab --------------------
with tabs[0]:
    st.write("Click an animated octopus pin to see the local date, time, weather & events!")

    m = folium.Map(
        location=[20, 0],
        zoom_start=2,
        tiles=tiles,
        min_zoom=2,
        max_zoom=5
    )

    for city, (lat, lon, tz_name, weather, event) in cities.items():
        tz = pytz.timezone(tz_name)
        real_time = datetime.datetime.now(tz)
        time_str = real_time.strftime('%Y-%m-%d %H:%M:%S')

        icon = DivIcon(
            html=f"""<div class="rotate" style="font-size: 24px;">🐙</div>"""
        )

        folium.Marker(
            location=[lat, lon],
            popup=f"<b>{city}</b><br>{time_str}<br>Weather: {weather}<br>Event: {event}",
            tooltip=f"{city}: {time_str}",
            icon=icon
        ).add_to(m)

    st_folium(m, width=1200, height=600)

# -------------------- Alarm tab --------------------
with tabs[1]:
    st.subheader("⏰ Alarm")
    alarm_time = st.time_input("Set Alarm Time")
    now_my = datetime.datetime.now(malaysia_tz).time()
    if st.button("Check Alarm"):
        if now_my.hour == alarm_time.hour and now_my.minute == alarm_time.minute:
            st.success("🔔 It’s alarm time! Wake up!")
            st.audio("https://www.soundjay.com/button/beep-07.wav", format="audio/wav", start_time=0)
        else:
            st.info(f"Current Malaysia time: {now_my.strftime('%H:%M:%S')} — Not yet!")

# -------------------- Stopwatch tab --------------------
with tabs[2]:
    st.subheader("⏱️ Stopwatch")
    if "stopwatch_running" not in st.session_state:
        st.session_state.stopwatch_running = False
        st.session_state.start_time = None
        st.session_state.elapsed = 0.0

    col1, col2, col3 = st.columns(3)

    if col1.button("Start/Resume Stopwatch"):
        if not st.session_state.stopwatch_running:
            st.session_state.start_time = time.time() - st.session_state.elapsed
            st.session_state.stopwatch_running = True

    if col2.button("Pause Stopwatch"):
        if st.session_state.stopwatch_running:
            st.session_state.elapsed = time.time() - st.session_state.start_time
            st.session_state.stopwatch_running = False

    if col3.button("Reset Stopwatch"):
        st.session_state.stopwatch_running = False
        st.session_state.start_time = None
        st.session_state.elapsed = 0.0

    if st.session_state.stopwatch_running:
        st.session_state.elapsed = time.time() - st.session_state.start_time

    st.write(f"Elapsed Time: {round(st.session_state.elapsed, 1)} seconds")

# -------------------- Timer tab --------------------
with tabs[3]:
    st.subheader("⏳ Timer")
    timer_duration = st.number_input("Set Timer (seconds)", min_value=1, value=10)
    if "timer_started" not in st.session_state:
        st.session_state.timer_started = False
        st.session_state.timer_start_time = None

    if st.button("Start Timer"):
        st.session_state.timer_started = True
        st.session_state.timer_start_time = time.time()

    if st.session_state.timer_started:
        elapsed = time.time() - st.session_state.timer_start_time
        remaining = max(0, timer_duration - elapsed)
        st.write(f"Time Remaining: {round(remaining, 1)} seconds")

        # Play ticking sound
        st.markdown(
            """
            <audio autoplay loop>
            <source src="https://www.soundjay.com/clock/sounds/clock-ticking-1.mp3" type="audio/mpeg">
            </audio>
            """,
            unsafe_allow_html=True
        )

        if remaining <= 0:
            st.success("⏳ Timer Done!")
            st.session_state.timer_started = False