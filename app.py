import streamlit as st
import requests
import os
from dotenv import load_dotenv

if 'count' not in st.session_state:
    st.session_state.count = 0
load_dotenv()

@st.cache_resource
def get_data(city):
    st.session_state.count += 1
    api_key = os.getenv("API_KEY")
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    response = requests.get(url)
    return response

def display(city, response):
    if response.status_code == 200:
        data = response.json()
        icon = data['weather'][0]['icon']
        main = data['weather'][0]['main']
        descr = data['weather'][0]['description']
        temperature = data['main']['temp']
        humidity = data['main']['humidity']
        pressure = data['main']['pressure']

        # Convert temperature from Kelvin to Celsius
        temperature_celsius = round(temperature - 273.15, 2)

        # Display the weather forecast
        st.subheader(f"Weather in :green[{city}]")
        st.image(f'https://openweathermap.org/img/wn/{icon}.png')
        st.write(f":blue[Temperature:] :green[{temperature_celsius}°C]")
        st.write(f":blue[Description:] :green[{descr}]")
        st.write(f":blue[Status:] :green[{main}]")
        st.write(f":blue[Humidity:] :green[{humidity}%]")
        st.write(f":blue[Pressure:] :green[{pressure} hPa]")
    else:
        st.error("Error fetching weather data. Please check the city name ")

def main():
    st.title("Weather App")
    city = st.text_input("Enter city name", "Bangalore").capitalize()
    response = get_data(city)
    display(city, response)
    print(f"Number of API requests made: {st.session_state.count}")

if __name__ == "__main__":
    main()
