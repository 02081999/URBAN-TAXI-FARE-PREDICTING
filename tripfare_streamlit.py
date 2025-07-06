#Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
#.\env\Scripts\Activate.ps1


import pandas as pd
import numpy as np
import pickle
import streamlit as st
from datetime import datetime
from datetime import time

st.set_page_config(
    page_title="🚗TAXI FARE PREDICTION",
    page_icon="assets/taxi.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load the trained model
with open(r'C:\Users\iswar\Music\GUVI PROJECTS\PROJECT_3\FILE\best_model.pkl', 'rb') as file:
    model = pickle.load(file)


# Title
# Load Google Font
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&display=swap" rel="stylesheet">

    <style>
    .custom-title {
        font-family: 'Bebas Neue', sans-serif;
        font-size: 60px;
        font-weight: bold;
        color: #FFCC00;
        text-align: center;
        margin-top: 20px;
        margin-bottom: 20px;
        letter-spacing: 2px;
    }
    </style>
    <div class="custom-title">🚖TAXI FARE PREDICTION</div>
""", unsafe_allow_html=True)


# Create three columns evenly spaced
col1, space1,col2, space2, col3 = st.columns([0.4, 0.1, 0.4, 0.1,0.4])

# Column 1
with col1:
    st.markdown("""<h3> 🚗Ride Information</h3>""",unsafe_allow_html=True)
    passenger_count =  st.selectbox("Passengers Count", ["1", "2", "3", "4","5","6","7"])
    trip_distance = st.number_input("Trip Distance (km)", min_value=0.0, format="%.2f")
    payment_type = st.selectbox("Payment Types", ["1 (UPI)", "2 (Cash)", "3 (Credit card)", "4 (Debit card)"])    
    payment_type = int(payment_type.split()[0])  # Extract number

# Column 2
with col2:
    st.markdown("""<h3> 💵Charges</h3>""",unsafe_allow_html=True)
    extra = st.number_input("Extra charges due to peak time", min_value=0.0, format="%.2f")
    tip_amount = st.number_input("Tip Amount", min_value=0.0, format="%.2f")
    tolls_amount = st.number_input("Tolls Amount", min_value=0.0, format="%.2f")


# Column 3
with col3:
    st.markdown("""<h3> 📅🕒Trip Date & Time</h3>""",unsafe_allow_html=True)
    now = datetime.now()
    selected_date = st.date_input("Select Date", value=now.date(), min_value=now.date())
    selected_time = st.time_input("Select Time", value=time(now.hour, now.minute))

    user_datetime = datetime.combine(selected_date, selected_time)
    pickup_dayofweek = user_datetime.weekday()
    hour = user_datetime.hour
    am_pm = 0 if hour < 12 else 1
    is_night = 1 if hour >= 22 or hour <= 5 else 0


    
st.markdown("""<style>
    div.stButton > button {
        display: block;
        margin: 20px auto;
        width: 60%;
        height: 60px;
        font-size: 100px;
        color: #000000;
        font-weight: 600;
        background-color: #FFD700;
        padding: 12px 24px;
        border-radius: 10px;
        border: none;
        cursor: pointer;
        transition: background-color 0.3s ease, transform 0.2s ease;
    }

    div.stButton > button:hover {
        background-color: #FFC300;
        color: #111111;
        transform: scale(1.03);
    }

    div.stButton > button:active {
        background-color: #E0B000;
        transform: scale(0.98);
    }
</style>
""", unsafe_allow_html=True)



if st.button("#### PREDICT FARE"):
             
        input_data = pd.DataFrame([{
        "passenger_count": passenger_count,
        "payment_type": payment_type,
        "extra": extra,
        "tip_amount": tip_amount,
        "tolls_amount": tolls_amount,
        "trip_distance": trip_distance,
        "pickup_dayofweek": pickup_dayofweek,
        "am_pm": am_pm,
        "hour": hour,
        "is_night": is_night
        }])


        # Convert appropriate columns to numeric
        input_data['passenger_count'] = input_data['passenger_count'].astype(int)
        input_data['tip_amount'] = input_data['tip_amount'].astype(float)
        input_data['tolls_amount'] = input_data['tolls_amount'].astype(float)
        input_data['trip_distance'] = input_data['trip_distance'].astype(float)
        input_data['hour'] = input_data['hour'].astype(int)
        input_data['is_night'] = input_data['is_night'].astype(int)

         # Convert categorical string columns if model was trained with them as categories
        categorical_cols = ['payment_type', 'extra', 'pickup_dayofweek', 'am_pm']
        for col in categorical_cols:            
            input_data[col] = input_data[col].astype('category')

        # Apply log transformation to distance
        input_data['trip_distance'] = np.log1p(input_data['trip_distance'])    

        #predicting fare
        prediction = model.predict(input_data)[0]
        st.success(f"Predicted Fare: ${prediction:.2f}")







   
    