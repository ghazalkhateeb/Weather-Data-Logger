# Weather Data Logger

1-please note that the code has an in-depth explanation about the functionalities of each method (in comments).

2-Please make sure to import all of the used libraries, including:

   * in app.py:

       from flask import Flask, render_template, request
       from weather_functions import get_json_from_openweathermap, display_weather_info

  * in weather_functions.py:

       import base64
       from io import BytesIO
       import matplotlib.pyplot as plt
       import pandas as pd
       import requests

   
3-to run the program:
   1- navigate to the pycharm's terminal
   2- run the following command: python app.py


