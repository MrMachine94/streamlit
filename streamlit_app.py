from select import select
import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import plotly.express as px

DATA_URL = (
"https://raw.githubusercontent.com/MrMachine94/streamlit/main/Motor_Vehicle_Collisions_-_Crashes.csv"
)
st.title("Motor Vehicle Collisions in New York City 🗽💥")
st.markdown("This application is a Streamlit Dashboard that can be used "
"to analyze motor vehicle collisions in NYC.")

# Cache is important for any running data not too overload and slow the operation
@st.cache(persist = True)
def load_data(nrows) :
    data = pd.read_csv(DATA_URL, nrows = nrows, parse_dates = [["CRASH_DATE", "CRASH_TIME"]])
    data.dropna(subset = ["LATITUDE", "LONGITUDE"], inplace = True)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis = "columns", inplace = True)
    data.rename(columns={"crash_date_crash_time" : "date/time"}, inplace = True)
    return data

data = load_data(100000)
original_data = data

# The 1st question here using st.header
st.header("Where are the most people injured in NYC?")

injured_people = st.slider("Number of Person injured in Vehicle Collision:",0, 19) # Slider minimum number and maximum 19
# Plot Data in map / filtering injured person and na values
st.map(data.query("injured_persons >= @injured_people")[["latitude", "longitude"]].dropna(how =  "any")) #lowercase operation

# The 2nd question
st.header("How many collisions occur during a given time of day")
# More interactive using dropdown selectbox
hour = st.selectbox("Hour to look at:", range(0,24),1)
# Slider type -> hour = st.slider("Hour to look at:", 0,23)
# Data to parse in 2nd question selectbox dropdown
data = data[data["date/time"].dt.hour == hour]

st.markdown("Vehicle collisions between %i:00 and %i:00" % (hour,(hour + 1) %24))
# Initial coordinate for new york city by calculating midpoint of longitude and langitude
midpoint = (np.average(data["latitude"]),np.average(data["longitude"]))

st.write(pdk.Deck(
    map_style = "mapbox://styles/mapbox/light-v9",
    initial_view_state = {
        "latitude":midpoint[0],
        "longitude":midpoint[1],
        #Degree of freedom for zoom pitch
        "zoom": 11,
        "pitch" : 50,
    },
    # Data points for 3D plot
    layers=[
        pdk.Layer(
            "HexagonLayer",
            # Subset of data with time interval
            data = data[["date/time", 'latitude', "longitude"]],
            get_position = ["longitude", "latitude"],
            radius = 100,
            extruded = True,
            pickable = True,
            elevation_scale = 4,
            elevation_range = [0, 1000],
        ),
    ],   
))
# Plotly barchart / histogram from line 70 to 77
st.subheader("Breakdown by minute between %i:00 and %i:00" % (hour, (hour + 1) %24))
filtered = data[
    (data["date/time"].dt.hour >= hour) & (data["date/time"].dt.hour < (hour+1))
]
hist = np.histogram(filtered["date/time"].dt.minute, bins=60, range=(0,60))[0]
chart_data = pd.DataFrame({"minute": range(60), "crashes": hist})
fig = px.bar(chart_data, x="minute", y="crashes", hover_data=["minute","crashes"], height=400)
st.write(fig)

# Select data using dropdowns
st.header("Top 5 of dangerous streets affected type")
select = st.selectbox("Affected type of people:", ["Pedestrians","Cyclists","Motorists"])

if select == "Pedestrians":
    st.write(original_data.query("injured_pedestrians >= 1")[["on_street_name","injured_pedestrians"]].sort_values(by=["injured_pedestrians"], ascending = False).dropna(how = "any")[:5])

# You can make a sidebar part with syntax st.sidebar.checkbox
# Checkbox of raw data
if st.checkbox("Show Raw Data", False):
    st.subheader("Raw Data")
    st.write(data)