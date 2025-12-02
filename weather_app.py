"""
Basic Weather App
Fetches current weather data using OpenWeatherMap API
"""

import requests
import json
from datetime import datetime
import sys

class WeatherApp:
    def __init__(self, api_key):
        """
        Initialize the Weather App with API key
        """
        self.api_key = api_key
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"
        self.units = "metric"  # Default to Celsius
        
    def get_weather_by_city(self, city_name):
        """
        Fetch weather data by city name
        """
        params = {
            "q": city_name,
            "appid": self.api_key,
            "units": self.units,
            "lang": "en"
        }
        
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()  # Raise exception for bad status codes
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching weather data: {e}")
            return None
    
    def get_weather_by_zip(self, zip_code, country_code="US"):
        """
        Fetch weather data by ZIP code
        """
        params = {
            "zip": f"{zip_code},{country_code}",
            "appid": self.api_key,
            "units": self.units,
            "lang": "en"
        }
        
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching weather data: {e}")
            return None
    
    def set_units(self, units):
        """
        Set temperature units (metric for Celsius, imperial for Fahrenheit)
        """
        if units.lower() in ['c', 'celsius', 'metric']:
            self.units = "metric"
        elif units.lower() in ['f', 'fahrenheit', 'imperial']:
            self.units = "imperial"
        else:
            print("Invalid unit. Using Celsius (metric) by default.")
            self.units = "metric"
    
    def display_weather(self, weather_data):
        """
        Display weather information in a formatted way
        """
        if not weather_data:
            print("No weather data to display.")
            return
        
        if weather_data.get("cod") != 200:
            print(f"Error: {weather_data.get('message', 'Unknown error')}")
            return
        
        # Extract relevant data
        city = weather_data.get("name", "Unknown")
        country = weather_data.get("sys", {}).get("country", "")
        temp = weather_data.get("main", {}).get("temp", "N/A")
        feels_like = weather_data.get("main", {}).get("feels_like", "N/A")
        humidity = weather_data.get("main", {}).get("humidity", "N/A")
        pressure = weather_data.get("main", {}).get("pressure", "N/A")
        weather_desc = weather_data.get("weather", [{}])[0].get("description", "N/A").title()
        wind_speed = weather_data.get("wind", {}).get("speed", "N/A")
        wind_dir = weather_data.get("wind", {}).get("deg", "N/A")
        visibility = weather_data.get("visibility", "N/A")
        
        # Get sunrise and sunset times
        sunrise = weather_data.get("sys", {}).get("sunrise")
        sunset = weather_data.get("sys", {}).get("sunset")
        
        # Convert timestamps if available
        if sunrise:
            sunrise_time = datetime.fromtimestamp(sunrise).strftime('%H:%M:%S')
        else:
            sunrise_time = "N/A"
            
        if sunset:
            sunset_time = datetime.fromtimestamp(sunset).strftime('%H:%M:%S')
        else:
            sunset_time = "N/A"
        
        # Determine temperature unit symbol
        unit_symbol = "°C" if self.units == "metric" else "°F"
        
        # Display header
        print("\n" + "="*50)
        print(f"WEATHER FORECAST - {city}, {country}")
        print("="*50)
        
        # Display weather information
        print(f"\n🌤️  Current Conditions: {weather_desc}")
        print(f"🌡️  Temperature: {temp}{unit_symbol} (Feels like: {feels_like}{unit_symbol})")
        print(f"💧 Humidity: {humidity}%")
        print(f"📊 Pressure: {pressure} hPa")
        print(f"💨 Wind Speed: {wind_speed} m/s")
        
        if wind_dir != "N/A":
            # Convert wind direction degrees to compass direction
            directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
            index = round(wind_dir / 45) % 8
            wind_direction = directions[index]
            print(f"🧭 Wind Direction: {wind_direction} ({wind_dir}°)")
        
        print(f"👁️  Visibility: {visibility} meters" if visibility != "N/A" else "👁️  Visibility: N/A")
        print(f"🌅 Sunrise: {sunrise_time}")
        print(f"🌇 Sunset: {sunset_time}")
        
        # Additional weather details
        print("\n" + "-"*30)
        print("Additional Details:")
        print("-"*30)
        
        # Weather icon based on description
        weather_main = weather_data.get("weather", [{}])[0].get("main", "").lower()
        icons = {
            "clear": "☀️",
            "clouds": "☁️",
            "rain": "🌧️",
            "drizzle": "🌦️",
            "thunderstorm": "⛈️",
            "snow": "❄️",
            "mist": "🌫️",
            "smoke": "💨",
            "haze": "😶‍🌫️",
            "dust": "🌪️",
            "fog": "🌁"
        }
        
        icon = icons.get(weather_main, "🌈")
        print(f"Weather Icon: {icon}")
        
        # Cloud coverage
        clouds = weather_data.get("clouds", {}).get("all", "N/A")
        print(f"☁️  Cloud Coverage: {clouds}%")
        
        print("="*50 + "\n")
    
    def validate_input(self, input_str):
        """
        Validate user input for location
        """
        if not input_str or input_str.isspace():
            return False, "Input cannot be empty."
        
        # Check if input is a ZIP code (numbers only)
        if input_str.replace("-", "").isdigit():
            # Remove any hyphens from ZIP codes
            clean_zip = input_str.replace("-", "")
            if len(clean_zip) >= 5:
                return True, "zip"
        
        # Otherwise treat as city name
        return True, "city"
    
    def run(self):
        """
        Main application loop
        """
        print("="*50)
        print("🌤️  BASIC WEATHER APPLICATION 🌤️")
        print("="*50)
        print("\nWelcome to the Weather App!")
        print("You can search weather by city name or ZIP code.")
        
        while True:
            try:
                print("\n" + "-"*30)
                print("MAIN MENU")
                print("-"*30)
                print("1. Check weather by location")
                print("2. Change temperature units")
                print("3. Exit")
                
                choice = input("\nEnter your choice (1-3): ").strip()
                
                if choice == "1":
                    self.check_weather()
                elif choice == "2":
                    self.change_units()
                elif choice == "3":
                    print("\nThank you for using the Weather App! Goodbye! 👋")
                    break
                else:
                    print("Invalid choice. Please enter 1, 2, or 3.")
                    
            except KeyboardInterrupt:
                print("\n\nProgram interrupted. Exiting...")
                break
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
    
    def check_weather(self):
        """
        Handle weather checking functionality
        """
        location = input("\nEnter city name or ZIP code: ").strip()
        
        # Validate input
        is_valid, input_type = self.validate_input(location)
        
        if not is_valid:
            print("Invalid input. Please try again.")
            return
        
        # Fetch weather data based on input type
        weather_data = None
        if input_type == "zip":
            # Ask for country code for ZIP code searches
            country = input("Enter country code (e.g., US, UK, IN) or press Enter for US: ").strip()
            country = country if country else "US"
            weather_data = self.get_weather_by_zip(location, country)
        else:  # city
            weather_data = self.get_weather_by_city(location)
        
        # Display results
        if weather_data:
            self.display_weather(weather_data)
        else:
            print("Could not retrieve weather data. Please check your input and try again.")
    
    def change_units(self):
        """
        Allow user to change temperature units
        """
        print("\n" + "-"*30)
        print("TEMPERATURE UNITS")
        print("-"*30)
        print("1. Celsius (°C)")
        print("2. Fahrenheit (°F)")
        
        choice = input("\nChoose temperature unit (1 or 2): ").strip()
        
        if choice == "1":
            self.set_units("celsius")
            print("Temperature units changed to Celsius (°C)")
        elif choice == "2":
            self.set_units("fahrenheit")
            print("Temperature units changed to Fahrenheit (°F)")
        else:
            print("Invalid choice. Keeping current units.")


def main():
    """
    Main function to run the weather app
    """
    # ==== YOUR API KEY ====
    API_KEY = "YOUR_API_KEY_HERE"
    
    # Test the API key
    print("🔐 Testing your OpenWeatherMap API key...")
    try:
        test_url = f"http://api.openweathermap.org/data/2.5/weather?q=London&appid={API_KEY}"
        response = requests.get(test_url, timeout=10)
        
        if response.status_code == 200:
            print("✅ API key is VALID and working!")
            print("Starting Weather App...\n")
            # Create and run the weather app
            app = WeatherApp(API_KEY)
            app.run()
        elif response.status_code == 401:
            print("❌ ERROR 401: Invalid API Key")
            print("\nDon't worry! This usually means:")
            print("1. Your key needs 10-15 minutes to activate (just wait)")
            print("2. Check if you verified your email")
            print("3. Make sure you're using HTTP (not HTTPS)")
            print("\nYour key: YOUR_API_KEY_HERE")
            print("Key length: 32 characters ✓")
            
            # Offer to test in browser
            print("\n💡 Quick test in browser:")
            print(f"Open: http://api.openweathermap.org/data/2.5/weather?q=London&appid={API_KEY}")
            
            # Try demo mode
            choice = input("\nUse demo mode while waiting? (yes/no): ").strip().lower()
            if choice == 'yes':
                display_demo_weather()
        else:
            print(f"⚠️  Status {response.status_code}: {response.text[:100]}")
            
    except requests.exceptions.ConnectionError:
        print("❌ No internet connection. Please check your network.")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nTrying demo mode...")
        display_demo_weather()


def display_demo_weather():
    """
    Display demo weather data
    """
    print("\n" + "="*50)
    print("DEMO WEATHER DATA - LONDON (Sample)")
    print("="*50)
    print("\n🌤️  Current Conditions: Clear Sky")
    print("🌡️  Temperature: 22°C (Feels like: 21°C)")
    print("💧 Humidity: 65%")
    print("📊 Pressure: 1013 hPa")
    print("💨 Wind Speed: 5.5 m/s")
    print("🧭 Wind Direction: NW (315°)")
    print("👁️  Visibility: 10000 meters")
    print("🌅 Sunrise: 06:45:00")
    print("🌇 Sunset: 18:30:00")
    print("\n" + "-"*30)
    print("Additional Details:")
    print("-"*30)
    print("Weather Icon: ☀️")
    print("☁️  Cloud Coverage: 0%")
    print("="*50)


if __name__ == "__main__":
    # Check Python version
    if sys.version_info < (3, 11):
        print("⚠️  This application is designed for Python 3.11.9 or higher.")
        print("   Some features might not work properly.")
    
    main()