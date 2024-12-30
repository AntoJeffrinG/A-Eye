import requests
from geopy.geocoders import Nominatim

# Function to get user's current location based on IP (optional: GPS integration for mobile)
def get_location():
    geolocator = Nominatim(user_agent="geoapiExercises")
    # For mobile applications, use device GPS APIs to get latitude and longitude instead
    try:
        response = requests.get("https://ipinfo.io")  # Gets IP-based location (can be replaced with GPS)
        data = response.json()
        location = data['loc'].split(',')
        latitude, longitude = location[0], location[1]
        return latitude, longitude
    except Exception as e:
        print(f"Error fetching location: {e}")
        return None

# Function to fetch weather data from the OpenWeatherMap API
def get_weather(latitude, longitude, api_key):
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}lat={latitude}&lon={longitude}&appid={api_key}&units=metric"
    
    # Sending a GET request to the API
    response = requests.get(complete_url)
    
    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        
        # Extracting necessary weather information
        main = data['main']
        weather_desc = data['weather'][0]['description']
        temperature = main['temp']
        humidity = main['humidity']
        
        # Return the weather details
        return f"Current weather: {weather_desc}, Temperature: {temperature}°C, Humidity: {humidity}%."
    else:
        return "Unable to fetch weather details."

# Example usage
if __name__ == "__main__":
    api_key = "9d03c0c0d3f5626d2d44b8952b1474c8"  # Replace this with your actual OpenWeatherMap API key
    location = get_location()
    if location:
        latitude, longitude = location
        weather_info = get_weather(latitude, longitude, api_key)
        print(weather_info)
"""import requests

# Function to fetch weather data from the OpenWeatherMap API for Chennai
def get_weather(api_key):
    latitude = 13.0827  # Latitude for Chennai
    longitude = 80.2707  # Longitude for Chennai
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}lat={latitude}&lon={longitude}&appid={api_key}&units=metric"
    
    # Sending a GET request to the API
    response = requests.get(complete_url)
    
    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        
        # Extracting necessary weather information
        main = data['main']
        weather_desc = data['weather'][0]['description']
        temperature = main['temp']
        humidity = main['humidity']
        
        # Return the weather details
        return f"Current weather in Chennai: {weather_desc}, Temperature: {temperature}°C, Humidity: {humidity}%."
    else:
        return "Unable to fetch weather details for Chennai."

# Example usage
if __name__ == "__main__":
    api_key = "9d03c0c0d3f5626d2d44b8952b1474c8"  # Replace this with your actual OpenWeatherMap API key
    weather_info = get_weather(api_key)
    print(weather_info)"""
