import speech_recognition as sr
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from twilio.rest import Client

# Twilio setup
TWILIO_ACCOUNT_SID = "AC7d5f3dcf60eca8783f26b0de892b2b13"  # Replace with your Twilio Account SID
TWILIO_AUTH_TOKEN = "aac3fdce6300cc359f2caeb8143d8368"    # Replace with your Twilio Auth Token
TWILIO_PHONE_NUMBER = "+12185027793 " # Replace with your Twilio phone number
CONTACT_PHONE_NUMBER = "+919150945499" # Replace with the emergency contact's phone number

# Initialize recognizer and geolocator
recognizer = sr.Recognizer()
geolocator = Nominatim(user_agent="EmergencyDetector")

# Function to fetch the current location
import requests

def get_current_location():
    try:
        # IP-based geolocation using ipinfo.io API
        response = requests.get('https://ipinfo.io')
        data = response.json()
        location = data['loc']  # Returns a string like "latitude,longitude"
        latitude, longitude = map(float, location.split(','))
        return latitude, longitude
    except Exception as e:
        print(f"Error fetching location: {e}")
        return None


# Function to send an emergency SMS alert
def send_emergency_sms(contact_number, latitude, longitude):
    try:
        # Create a Twilio client
        client = Client("AC1b5e6188bcd73beaec18333df0f4cc1c", "d21df37dd39d6b970a91c4393fdd7f25")

        # Prepare the SMS message content
        message_body = f"Emergency detected! The user is in danger. Current location: Latitude: {latitude}, Longitude: {longitude}"

        # Send the SMS message
        message = client.messages.create(  
            body=message_body,
            from_="+13522928291",
            to=contact_number
        )
        print(f"Emergency SMS sent to {+919150945499}.")
    except Exception as e:
        print(f"Failed to send the SMS: {e}")


# Function to recognize and process speech for emergency phrases
def recognize_speech():
    with sr.Microphone() as source:
        print("Listening for emergency phrases...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        audio = recognizer.listen(source)

    try:
        # Use Google's speech recognition to convert speech to text
        text = recognizer.recognize_google(audio)
        print(f"Recognized: {text}")

        # Process the text to check for emergency keywords
        emergency_keywords = ["help me", "i am in danger", "emergency"]
        if any(keyword.lower() in text.lower() for keyword in emergency_keywords):
            print("Emergency detected!")
            latitude, longitude = get_current_location()
            if latitude and longitude:
                send_emergency_sms(CONTACT_PHONE_NUMBER, latitude, longitude)
                print("Your location has been shared.")
            else:
                print("Failed to fetch the location.")
        else:
            print("No emergency keywords detected.")
    except sr.UnknownValueError:
        print("Sorry, I could not understand the speech.")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")

# Continuous listening loop
while True:
    recognize_speech()
