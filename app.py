from flask import Flask, render_template, request
from weather_functions import get_json_from_openweathermap, display_weather_info

#Creates a Flask application instance named 'app'.
app = Flask(__name__)

# Route to render the index page.
# This route specifies what happens when a user visits the root URL '/'.
# It triggers the index() function, which renders the index.html template.
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle form submission and fetch weather data.
# This route specifies how the application handles form submissions when the user requests weather data.
# It listens for POST requests sent to the '/weather' endpoint.
@app.route('/weather', methods=['POST'])
def weather():
    api_key = "f27bce02733af36b6022645dc5a55a2a"
    # Extract the location entered by the user from the submitted form
    location = request.form['location']
    weather_data = get_json_from_openweathermap(api_key, location)
    # Check if weather data was successfully fetched
    if weather_data:
        graph_image = display_weather_info(weather_data)
        return render_template('weather.html', location=location, weather_data=weather_data, graph_image=graph_image)
    else:
        return "Failed to fetch weather data"

# Route to navigate back to the home page.
# This route specifies how the application redirects users back to the home page.
# It listens for GET requests sent to the '/home' endpoint.
@app.route('/home', methods=['GET'])
def go_to_home():
    return render_template('index.html')

def main():
    app.run(debug=True)

if __name__ == '__main__':
    main()

