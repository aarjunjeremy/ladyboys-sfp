import streamlit as st
import pandas as pd
import datetime
import pytz
import time

# ----------------- Demo city data -----------------
cities = pd.DataFrame({
    'City': ['New York', 'London', 'Tokyo', 'Sydney'],
    'Lat': [40.7128, 51.5074, 35.6895, -33.8688],
    'Lon': [-74.0060, -0.1278, 139.6917, 151.2093],
    'Timezone': ['America/New_York', 'Europe/London', 'Asia/Tokyo', 'Australia/Sydney']
})

# ----------------- Helper Functions -----------------
def get_local_time(timezone_name):
    tz = pytz.timezone(timezone_name)
    now = datetime.datetime.now(tz)
    return now.strftime("%Y-%m-%d %H:%M:%S")

# ----------------- App -----------------
st.set_page_config(page_title="Clocktopus", layout="centered")

st.title("🐙 Clocktopus")
st.write("Your all-in-one World Clock, Alarm, Stopwatch, and Timer!")

# ----------------- Tabs -----------------
tab1, tab2, tab3 = st.tabs(["🌍 World Clock", "⏰ Alarm", "⏱️ Stopwatch & Timer"])

# ----------------- World Clock -----------------
with tab1:
    st.header("World Clock Map")

    # Show map with city points
    st.map(cities.rename(columns={"Lat": "latitude", "Lon": "longitude"}), zoom=1)

    selected_city = st.selectbox("Select a city:", cities['City'].unique())
    city_row = cities[cities['City'] == selected_city].iloc[0]
    local_time = get_local_time(city_row['Timezone'])

    st.success(f"Current time in {selected_city}: {local_time}")

# ----------------- Alarm -----------------
with tab2:
    st.header("Alarm Clock")

    alarm_time = st.time_input("Set alarm time:", value=datetime.time(7, 0))
    st.write(f"Alarm set for: {alarm_time.strftime('%H:%M:%S')}")

    if st.button("Start Alarm"):
        st.warning("Keep this page open! Streamlit can't run background alarms — this is a live simulation.")
        with st.spinner("Waiting for alarm time..."):
            while True:
                now = datetime.datetime.now().time()
                if now >= alarm_time:
                    st.success("⏰ Alarm! Time's up!")
                    break
                time.sleep(1)

# ----------------- Stopwatch & Timer -----------------
with tab3:
    st.header("Stopwatch")

    if "stopwatch_running" not in st.session_state:
        st.session_state.stopwatch_running = False
        st.session_state.stopwatch_start = None

    col1, col2, col3 = st.columns(3)
    if col1.button("Start"):
        st.session_state.stopwatch_running = True
        st.session_state.stopwatch_start = time.time()

    if col2.button("Stop"):
        st.session_state.stopwatch_running = False

    if col3.button("Reset"):
        st.session_state.stopwatch_running = False
        st.session_state.stopwatch_start = None

    if st.session_state.stopwatch_running:
        elapsed = time.time() - st.session_state.stopwatch_start
        st.write(f"Elapsed Time: {elapsed:.2f} seconds")
    elif st.session_state.stopwatch_start:
        elapsed = time.time() - st.session_state.stopwatch_start
        st.write(f"Stopped at: {elapsed:.2f} seconds")

    st.divider()

    st.header("Timer")
    timer_seconds = st.number_input("Set timer (seconds):", min_value=1, max_value=3600, value=10)

    if st.button("Start Timer"):
        with st.spinner("Counting down..."):
            for i in range(timer_seconds, 0, -1):
                st.write(f"⏳ {i} seconds remaining")
                time.sleep(1)
            st.success("⏰ Timer done!")


