import streamlit as st
import pandas as pd
import numpy as np
import pickle

# Load the model, encoders, and scaler
model = pickle.load(open('Model.pkl', 'rb'))
encoders = pickle.load(open('encoders.pkl', 'rb'))
scaler = pickle.load(open('scaler.pkl', 'rb'))

class CustomData:
    def __init__(self, 
                 Location: str, 
                 Cuisine: str, 
                 Rating: float, 
                 Seating_Capacity: int, 
                 Average_Meal_Price: float, 
                 Social_Media_Followers: int, 
                 Chef_Experience_Years: int, 
                 Number_of_Reviews: int, 
                 Avg_Review_Length: float, 
                 Ambience_Score: float, 
                 Service_Quality_Score: float, 
                 Parking_Availability: str, 
                 Weekend_Reservations: int, 
                 Weekday_Reservations: int):
        
        self.Location = Location
        self.Cuisine = Cuisine
        self.Rating = Rating
        self.Seating_Capacity = Seating_Capacity
        self.Average_Meal_Price = Average_Meal_Price
        self.Social_Media_Followers = Social_Media_Followers
        self.Chef_Experience_Years = Chef_Experience_Years
        self.Number_of_Reviews = Number_of_Reviews
        self.Avg_Review_Length = Avg_Review_Length
        self.Ambience_Score = Ambience_Score
        self.Service_Quality_Score = Service_Quality_Score
        self.Parking_Availability = Parking_Availability
        self.Weekend_Reservations = Weekend_Reservations
        self.Weekday_Reservations = Weekday_Reservations

    def get_data_as_dataframe(self):
        try:
            custom_data_input_dict = {
                'Location': [self.Location],
                'Cuisine': [self.Cuisine],
                'Rating': [self.Rating],
                'Seating Capacity': [self.Seating_Capacity],
                'Average Meal Price': [self.Average_Meal_Price],
                'Social Media Followers': [self.Social_Media_Followers],
                'Chef Experience Years': [self.Chef_Experience_Years],
                'Number of Reviews': [self.Number_of_Reviews],
                'Avg Review Length': [self.Avg_Review_Length],
                'Ambience Score': [self.Ambience_Score],
                'Service Quality Score': [self.Service_Quality_Score],
                'Parking Availability': [self.Parking_Availability],
                'Weekend Reservations': [self.Weekend_Reservations],
                'Weekday Reservations': [self.Weekday_Reservations]
            }
            df = pd.DataFrame(custom_data_input_dict)
            return df
        except Exception as e:
            raise Exception(f"Error in creating DataFrame: {e}")

# Define the inputs
st.title("Restaurant Revenue Prediction")

Location = st.selectbox('Location', ['Rural', 'Urban', 'Suburban'])
Cuisine = st.selectbox('Cuisine', ['Japanese', 'Italian', 'Mexican', 'Indian', 'Chinese'])
Rating = st.slider('Rating', 1.0, 5.0, step=0.1)
Seating_Capacity = st.number_input('Seating Capacity', min_value=1,  value=38)
Average_Meal_Price = st.number_input('Average Meal Price', min_value=1.0, value=73.98)
Social_Media_Followers = st.number_input('Social Media Followers', min_value=0, value=23406)
Chef_Experience_Years = st.number_input('Chef Experience Years', min_value=0, value=13)
Number_of_Reviews = st.number_input('Number of Reviews', min_value=0, value=185)
Avg_Review_Length = st.number_input('Avg Review Length', min_value=0.0, value=161.92)
Ambience_Score = st.number_input('Ambience Score', min_value=0.0, value=1.3)
Service_Quality_Score = st.number_input('Service Quality Score', min_value=0.0, value=7.0)
Parking_Availability = st.selectbox('Parking Availability', ['Yes', 'No'])
Weekend_Reservations = st.number_input('Weekend Reservations', min_value=0, value=13)
Weekday_Reservations = st.number_input('Weekday Reservations', min_value=0, value=4)

# Create an instance of the CustomData class
input_data = CustomData(
    Location, Cuisine, Rating, Seating_Capacity, Average_Meal_Price, Social_Media_Followers, 
    Chef_Experience_Years, Number_of_Reviews, Avg_Review_Length, Ambience_Score, 
    Service_Quality_Score, Parking_Availability, Weekend_Reservations, Weekday_Reservations
)

# Convert the input data to a DataFrame
input_df = input_data.get_data_as_dataframe()

# Encode categorical variables using the encoders
categorical_features = ['Location', 'Cuisine', 'Parking Availability']

# Predict revenue
if st.button('Predict Revenue'):
    for feature in categorical_features:
        input_df[feature] = encoders[feature].transform(input_df[feature])

# Scale the features
    scaled_input_data = scaler.transform(input_df)
    prediction = model.predict(scaled_input_data)
    st.write(f"Predicted Revenue: ${prediction[0]:,.2f}")
