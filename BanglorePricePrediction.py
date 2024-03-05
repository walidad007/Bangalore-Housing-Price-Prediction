import pickle
import json
import numpy as np
from os import path

# Define global variables to store data and model
availability_values = None
area_values = None
location_values = None
model = None

# Function to load saved attributes from files
def load_saved_attributes():
    global availability_values
    global location_values
    global area_values
    global model

    # Load data from JSON file
    with open("columns.json", "r") as f:
        resp = json.load(f)
        availability_values = resp["availability_columns"]
        area_values = resp["area_columns"]
        location_values = resp["location_columns"]

    # Load trained model from pickle file
    model = pickle.load(open("banglore_home_prices_model.pickle", "rb"))

# Function to get location names
def get_location_names():
    return location_values

# Function to get availability values
def get_availability_values():
    return availability_values

# Function to get area values
def get_area_values():
    return area_values

# Function to predict house price
def predict_house_price(location, area, availability, sqft, bhk, bathrooms):
    try:
        # Get the index of location, area, and availability from their respective lists
        loc_index = location_values.index(location)
        availability_index = availability_values.index(availability)
        area_index = area_values.index(area)
    except:
        loc_index = -1
        area_index = -1
        availability_index = -1

    # Create arrays with zeros and set 1 at the corresponding index
    loc_array = np.zeros(len(location_values))
    if loc_index >= 0:
        loc_array[loc_index] = 1

    area_array = np.zeros(len(area_values))
    if area_index >= 0:
        area_array[area_index] = 1

    availability_array = np.zeros(len(availability_values))
    if availability_index >= 0:
        availability_array[availability_index] = 1

    # Exclude the last element from arrays
    availability_array = availability_array[:-1]
    area_array = area_array[:-1]
    loc_array = loc_array[:-1]

    # Concatenate the arrays with other features (sqft, bhk, bathrooms)
    sample = np.concatenate((np.array([sqft, bhk, bathrooms]), availability_array, area_array, loc_array))

    # Predict house price using the trained model and return the prediction
    return model.predict(sample.reshape(1,-1))[0]

# Load saved attributes if the module is executed directly
if __name__ == '__main__':
    load_saved_attributes()
else:
    load_saved_attributes()
