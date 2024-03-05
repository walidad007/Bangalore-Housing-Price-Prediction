from flask import Flask, request, render_template, jsonify
from flask_cors import cross_origin
import BangalorePricePrediction as tm  # Import your custom module for Bangalore price prediction

app = Flask(__name__)

# Define route to get location names
@app.route('/get_location_names', methods=['GET'])
def get_location_names():
    # Get location names using a function from your custom module
    response = jsonify({
        'locations': tm.get_location_names()
    })
    # Allow cross-origin requests
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

# Define route to get area names
@app.route('/get_area_names', methods=['GET'])
def get_area_names():
    # Get area names using a function from your custom module
    response = jsonify({
        'area': tm.get_area_values()
    })
    # Allow cross-origin requests
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

# Define route to get availability names
@app.route('/get_availability_names', methods=['GET'])
def get_availability_names():
    # Get availability names using a function from your custom module
    response = jsonify({
        'availability': tm.get_availability_values()
    })
    # Allow cross-origin requests
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

# Define route for the home page
@app.route("/")
@cross_origin()  # Allow cross-origin requests
def home():
    return render_template("home.html")  # Render the home.html template

# Define route for the prediction functionality
@app.route("/predict", methods=["GET", "POST"])
def predict():
    if request.method == "POST":
        # Retrieve form data
        sqft = float(request.form['sqft'])
        bhk = int(request.form['bhk'])
        bath = int(request.form['bath'])
        loc = request.form.get('loc')
        area = request.form.get('area')
        availability = request.form.get('avail')

        # Predict house price using a function from your custom module
        prediction = round(float(tm.predict_house_price(loc, area, availability, sqft, bhk, bath)), 2)

        # Render the home.html template with the prediction result
        return render_template('home.html', prediction_text="The house price is Rs. {} lakhs".format(prediction))

    return render_template("home.html")  # Render the home.html template if the request method is not POST

# Load saved attributes and run the Flask application
if __name__ == "__main__":
    tm.load_saved_attributes()  # Load saved attributes from your custom module
    app.run(debug=True)  # Run the Flask application in debug mode
