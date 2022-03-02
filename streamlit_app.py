import streamlit as st
import pandas as pd
import numpy as np

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

# The question here using st.header
st.header("Where are the most people injured in NYC?")

injured_people = st.slider("Number of Person injured in Vehicle Collision:",0, 19) # Slider minimum number and maximum 19
# Plot Data in map / filtering injured person and na values
st.map(data.query("injured_persons >= @injured_people")[["latitude", "longitude"]].dropna(how =  "any")) #lowercase operation
# Checkbox of raw data
if st.checkbox("Show Raw Data", False):
    st.subheader("Raw Data")
    st.write(data)

