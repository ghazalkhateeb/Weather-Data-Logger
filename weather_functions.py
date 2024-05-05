import base64
from io import BytesIO

import matplotlib.pyplot as plt
import pandas as pd
import requests

# Switch matplotlib to non-interactive mode.
plt.switch_backend('agg')

def get_json_from_openweathermap(api_key, city):
    """
    Fetches weather data from the openWeatherMap API.

    Args:
         api_key: The API key to accessing the openWeatherMap API.
         city: The name of the city for which weather data is requested.

    Returns:
          A dictionary containing weather data if the request is successful,
             otherwise None.
    """

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    #Send a GET request to the openWeatherMap API.
    http_response = requests.get(url)
    #Check if the request was successful.
    if http_response.status_code == 200:
        #Extract JSON data from the HTTP response.
        weather_data = http_response.json()
        return weather_data
    else:
        print("Failed to fetch weather data")
        return None

def display_weather_info(weather_data):
    """
    Display weather information graphically.

    Args:
        weather_data (dict): JSON data obtained from the OpenWeatherMap API.

    Returns:
        str: Base64 encoded image representing the weather graph.
    """

    # Extract weather information from the provided data
    temperature = weather_data['main']['temp']
    humidity = weather_data['main']['humidity']
    wind_speed = weather_data['wind']['speed']

    # Create a Panda DataFrame containing weather metrics
    current_dataframe = pd.DataFrame({
        'Metric': ['Temperature', 'Humidity', 'Wind Speed'],
        'Value': [temperature, humidity, wind_speed]
    })

    # Plot the weather metrics
    plt.figure(figsize=(10, 5))
    plt.bar(current_dataframe['Metric'], current_dataframe['Value'])
    plt.xlabel('Metric Units')
    plt.ylabel('Measurement Value')
    plt.title('Weather Data')

    # Convert the plot to base64 format
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode()
    plt.close()
    return image_base64

