from flask import Flask, render_template, request
import requests #help python sending http request easily
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64

#creating the Flask app
app = Flask(__name__)

# switch matplotlib to non-interactive mode
plt.switch_backend('agg')

#this function takes two parameters: apiKey and city.
#this function sends an http request to the OpenWeatherMap API using the apiKey and the specified city to fetch data weather.
def getJsonFromOpenWeatherMap(apiKey, city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={apiKey}&units=metric"
    # send a get request to the url constructed in the prev line (OpenWeatherMap)
    httpResponse = requests.get(url)
    # 200 indicates successful request
    if httpResponse.status_code == 200:
        # extract the json from the http response
        weatherData = httpResponse.json()
        return weatherData
    #the request failed
    else:
        print("Failed")
        return None

#this function takes one parameter: theDataOfWeather, which is the json data that  obtained from the OpenWeatherMap API
#this function extracts relevant weather information (temperature, humidity and wind speed),
#and creates a graph using matplotlib.
def displayWeatherInfo(theDataOfWeather):
    # extracts the temperature data from the weather data JSON object
    temperature = theDataOfWeather['main']['temp']
    # extracts the humidity data from the weather data JSON object
    humidity = theDataOfWeather['main']['humidity']
    # extracts the windSpeed data from the weather data JSON object
    windSpeed = theDataOfWeather['wind']['speed']

    #create a panda DataFrame that contains three columns, temperature, humidity, windSpeed and the appropriate value.
    currentDataFrame = pd.DataFrame({
        'Metric': ['Temperature', 'Humidity', 'Wind Speed'],
        'Value': [temperature, humidity, windSpeed]
    })

    plt.figure(figsize=(10, 5))
    plt.bar(currentDataFrame['Metric'], currentDataFrame['Value'])
    plt.xlabel('Metric Units')
    plt.ylabel('Measurement Value')
    plt.title('Weather Data')
    # temporary memory
    buffer = BytesIO()
    # save the plot in the buffer
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    imageBase64 = base64.b64encode(buffer.read()).decode()
    plt.close()
    return imageBase64


#when the user visits the root URL '/', the index() function is executed.
@app.route('/')
def index():
    #return the index.html as a response
    return render_template('index.html')

#When the button "Enter Location" is pressed, this route is triggered.
@app.route('/weather', methods=['POST'])
def weather():
    apiKey = "f27bce02733af36b6022645dc5a55a2a"
    #extracts the location entered by the user
    location = request.form['location']
    # Fetch weather data using the getJsonFromOpenWeatherMap function
    weatherData = getJsonFromOpenWeatherMap(apiKey, location)
    # Generate the graph
    graphImage = displayWeatherInfo(weatherData)
    # Pass fetched data and graph to weather.html template
    return render_template('weather.html', location=location, weatherData=weatherData, graph_image=graphImage)

#When the button "Get back home" is pressed, this route is triggered.
@app.route('/', methods=['GET'])
def go_to_index():
    return render_template('index.html')

#run the flask app
if __name__ == '__main__':
    app.run(debug=True)
