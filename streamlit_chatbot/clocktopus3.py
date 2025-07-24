import streamlit as st
from streamlit_folium import st_folium
import folium
from folium.features import DivIcon
import datetime
import pytz
import google.generativeai as genai

# -------------------- CONFIGURE GEMINI --------------------
# Hardcode Gemini API Key for local testing
GOOGLE_API_KEY = "AIzaSyDNdCNP-GPm6CCzP3nma57H9-1AhEs_D58"
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# -------------------- Custom CSS + Autoplay Audio --------------------
st.markdown(
    """
    <style>
    body {
        background: url('https://images.unsplash.com/photo-1600585154340-be6161a56a0c?ixlib=rb-4.0.3&auto=format&fit=crop&w=1470&q=80') no-repeat center center fixed;
        background-size: cover;
    }
    .main {
        background-color: rgba(0,0,0,0.5);
        padding: 2rem;
        border-radius: 1rem;
    }
    .tentacle {
        display: inline-block;
        transition: all 0.4s ease-in-out;
    }
    .tentacle:hover {
        transform: rotate(20deg) scale(1.3);
    }
    .tentacle.pulse {
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { transform: scale(1);}
        50% { transform: scale(1.1);}
        100% { transform: scale(1);}
    }
    .subtext {
        font-size: 14px;
        color: #ccc;
    }
    </style>

    <!-- Autoplay background music (browser will block if no interaction) -->
    <audio autoplay loop>
      <source src="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3" type="audio/mpeg">
    </audio>
    """,
    unsafe_allow_html=True
)

# -------------------- Cities --------------------
cities = {
    "Kuala Lumpur": (3.1390, 101.6869, "Asia/Kuala_Lumpur"),
    "George Town": (5.4141, 100.3288, "Asia/Kuala_Lumpur"),
    "Johor Bahru": (1.4927, 103.7414, "Asia/Kuala_Lumpur"),
    "Tokyo": (35.6895, 139.6917, "Asia/Tokyo"),
    "Osaka": (34.6937, 135.5023, "Asia/Tokyo"),
    "Kyoto": (35.0116, 135.7681, "Asia/Tokyo"),
    "Sydney": (-33.8688, 151.2093, "Australia/Sydney"),
    "Melbourne": (-37.8136, 144.9631, "Australia/Melbourne"),
    "London": (51.5074, -0.1278, "Europe/London"),
    "Manchester": (53.4808, -2.2426, "Europe/London"),
    "Edinburgh": (55.9533, -3.1883, "Europe/London"),
    "New York": (40.7128, -74.0060, "America/New_York"),
    "Los Angeles": (34.0522, -118.2437, "America/Los_Angeles"),
    "Chicago": (41.8781, -87.6298, "America/Chicago"),
    "Miami": (25.7617, -80.1918, "America/New_York"),
    "San Francisco": (37.7749, -122.4194, "America/Los_Angeles"),
    "Paris": (48.8566, 2.3522, "Europe/Paris"),
    "Berlin": (52.52, 13.405, "Europe/Berlin"),
    "Munich": (48.1351, 11.5820, "Europe/Berlin"),
    "Rome": (41.9028, 12.4964, "Europe/Rome"),
    "Milan": (45.4642, 9.19, "Europe/Rome"),
    "Moscow": (55.7558, 37.6176, "Europe/Moscow"),
    "Saint Petersburg": (59.9311, 30.3609, "Europe/Moscow"),
    "Beijing": (39.9042, 116.4074, "Asia/Shanghai"),
    "Shanghai": (31.2304, 121.4737, "Asia/Shanghai"),
    "Bangkok": (13.7563, 100.5018, "Asia/Bangkok"),
    "Phuket": (7.8804, 98.3923, "Asia/Bangkok"),
    "Dubai": (25.276987, 55.296249, "Asia/Dubai"),
    "Abu Dhabi": (24.4539, 54.3773, "Asia/Dubai"),
    "Mumbai": (19.0760, 72.8777, "Asia/Kolkata"),
    "Delhi": (28.7041, 77.1025, "Asia/Kolkata"),
    "Singapore": (1.3521, 103.8198, "Asia/Singapore"),
    "Cape Town": (-33.9249, 18.4241, "Africa/Johannesburg"),
    "Istanbul": (41.0082, 28.9784, "Europe/Istanbul"),
    "Mexico City": (19.4326, -99.1332, "America/Mexico_City"),
    "Cancun": (21.1619, -86.8515, "America/Cancun"),
    "Toronto": (43.651070, -79.347015, "America/Toronto"),
    "Vancouver": (49.2827, -123.1207, "America/Vancouver"),
    "Rio de Janeiro": (-22.9068, -43.1729, "America/Sao_Paulo"),
    "Buenos Aires": (-34.6037, -58.3816, "America/Argentina/Buenos_Aires"),
    "Santiago": (-33.4489, -70.6693, "America/Santiago"),
    "Lima": (-12.0464, -77.0428, "America/Lima"),
    "Cairo": (30.0444, 31.2357, "Africa/Cairo"),
    "Nairobi": (-1.2921, 36.8219, "Africa/Nairobi"),
    "Lagos": (6.5244, 3.3792, "Africa/Lagos"),
    "Athens": (37.9838, 23.7275, "Europe/Athens"),
    "Helsinki": (60.1699, 24.9384, "Europe/Helsinki"),
}

# -------------------- Config --------------------
st.set_page_config(page_title="Clocktopus by Koli Curry", page_icon="🐙", layout="wide")
st.title("🐙 Clocktopus")
st.markdown('<div class="subtext">by Koli Curry</div>', unsafe_allow_html=True)
st.header("Time Zones in Every Tentacle!")

# -------------------- Tabs --------------------
tabs = st.tabs([
    "🌍 Map",
    "🌐 World Clock Converter",
    "🌊 Earth Stats",
    "🌏 Earth Facts",
])

# -------------------- Malaysia Time --------------------
malaysia_tz = pytz.timezone("Asia/Kuala_Lumpur")
if "snapshot" not in st.session_state:
    st.session_state.snapshot = datetime.datetime.now(malaysia_tz)
snapshot = st.session_state.snapshot

# -------------------- MAP --------------------
with tabs[0]:
    st.write("Click a wiggly tentacle to see frozen time snapshot!")

    m = folium.Map(
        location=[20, 0],
        zoom_start=2,
        tiles="CartoDB dark_matter",
        min_zoom=2,
        max_zoom=5
    )

    for city, (lat, lon, tz_name) in cities.items():
        tz = pytz.timezone(tz_name)
        local_time = snapshot.astimezone(tz)
        time_str = local_time.strftime('%Y-%m-%d %H:%M:%S')
        icon = DivIcon(
            html=f"""<div class="tentacle pulse" style="font-size:24px;">🐙</div>"""
        )
        folium.Marker(
            location=[lat, lon],
            popup=f"<b>{city}</b><br>{time_str}",
            tooltip=f"{city}: {time_str}",
            icon=icon
        ).add_to(m)

    st_folium(m, width=1200, height=600)

# -------------------- WORLD CLOCK CONVERTER --------------------
with tabs[1]:
    st.subheader("🌐 World Clock Converter")
    city1 = st.selectbox("City 1", list(cities.keys()), index=0)
    city2 = st.selectbox("City 2", list(cities.keys()), index=1)
    tz1 = pytz.timezone(cities[city1][2])
    tz2 = pytz.timezone(cities[city2][2])
    time1 = snapshot.astimezone(tz1)
    time2 = snapshot.astimezone(tz2)
    col1, col2 = st.columns(2)
    col1.metric(f"{city1}", f"{time1.strftime('%Y-%m-%d %H:%M:%S')}")
    col2.metric(f"{city2}", f"{time2.strftime('%Y-%m-%d %H:%M:%S')}")

# -------------------- EARTH STATS --------------------
with tabs[2]:
    st.subheader("🌊 Earth Stats Dashboard")
    st.write("**Live, real-world stats to remind us how our tentacles connect to Earth!**")
    st.metric("🌍 World Population", "8,080,000,000")
    st.metric("🌿 CO₂ Emissions This Year", "~36 billion tonnes")
    st.metric("♻️ Ocean Plastic Waste This Year", "~8 million tonnes")
    st.metric("🌅 Sunrise & Sunset (KL)", "7:00 AM / 7:15 PM")
    if st.button("🔄 Refresh Earth Stats"):
        st.session_state.snapshot = datetime.datetime.now(malaysia_tz)
        st.experimental_rerun()

# -------------------- EARTH FACTS with MEMORY --------------------
with tabs[3]:
    st.subheader("🌏 Get a Fresh Earth Fact (No Repeats)")

    if "earth_fact" not in st.session_state:
        st.session_state.earth_fact = "Press the button to get your first Earth fact!"
    if "fact_history" not in st.session_state:
        st.session_state.fact_history = []

    if st.button("✨ New Earth Fact"):
        # Build prompt with previous facts
        previous = "\n".join(st.session_state.fact_history)
        prompt = f"""
        You are a helpful Earth fact generator.
        Here is what you have already told me:
        {previous if previous else '[None yet]'}
        Now give me 1 unique, surprising, scientifically accurate fact about Earth 
        that is NOT on this list, keep it under 50 words.
        """

        response = model.generate_content(prompt)
        new_fact = response.text.strip()

        # Store new fact
        st.session_state.fact_history.append(new_fact)
        st.session_state.earth_fact = new_fact

    st.success(st.session_state.earth_fact)
