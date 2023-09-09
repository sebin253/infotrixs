import json
import sys
import requests
import time
import os  # Import the os module for file checking

# API key for OpenWeatherMap (replace with your own)
API_KEY = "c471b3ac1ab984fd39c58d30b92fbbe5"

# Initialize a list to store favorite cities
favorite_cities = []

# Check if the "favorite_cities.json" file exists
if os.path.exists("favorite_cities.json"):
    # Load favorite cities from the JSON file (if it exists and is not empty)
    with open("favorite_cities.json", "r") as file:
        try:
            favorite_cities = json.load(file)
        except json.JSONDecodeError:
            # Handle the case where the file is empty or not valid JSON
            pass

def save_favorite_cities():
    with open("favorite_cities.json", "w") as file:
        json.dump(favorite_cities, file)

def get_weather(location):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={API_KEY}"
        response = requests.get(url)
        response.raise_for_status()
        weather_data = json.loads(response.text)

        data = weather_data['weather'][0]
        description = data['description'].capitalize()
        temperature = weather_data['main']['temp'] - 273.15  # Convert to Celsius

        print(f"Current weather in {location}:")
        print(f"Weather: {data['main']} - {description}")
        print(f"Temperature: {temperature:.2f}°C")
        print()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
    except KeyError:
        print("Error: Invalid location or data not found.")

def add_favorite(city):
    if city not in favorite_cities:
        favorite_cities.append(city)
        print(f"{city} added to favorites.")
        save_favorite_cities()  # Save the updated list to the JSON file
    else:
        print(f"{city} is already in your favorites.")
    print("Current list of favorites:", favorite_cities)

def list_favorites():
    if favorite_cities:
        print("Your favorite cities:")
        for city in favorite_cities:
            print(city)
    else:
        print("You don't have any favorite cities yet.")

def remove_favorite(city):
    if city in favorite_cities:
        favorite_cities.remove(city)
        save_favorite_cities()
        print(f"{city} removed from favorites.")
    else:
        print(f"{city} is not in your favorites.")

def update_favorite(old_city_name, new_city_name):
    if old_city_name in favorite_cities:
        index = favorite_cities.index(old_city_name)
        favorite_cities[index] = new_city_name
        save_favorite_cities()
        print(f"Updated {old_city_name} to {new_city_name}.")
    else:
        print(f"{old_city_name} is not in your favorites.")


def auto_refresh(interval):
    while True:
        for city in favorite_cities:
            get_weather(city)
        time.sleep(interval)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: weather.py <command> [options]")
        sys.exit()

    command = sys.argv[1].lower()

    if command == "check":
        if len(sys.argv) < 3:
            print("Usage: weather.py check <city>")
        else:
            location = ' '.join(sys.argv[2:])
            get_weather(location)
    elif command == "add":
        if len(sys.argv) < 3:
            print("Usage: weather.py add <city>")
        else:
            city_to_add = ' '.join(sys.argv[2:])
            add_favorite(city_to_add)
    elif command == "update":
        if len(sys.argv) < 4:
            print("Usage: weather.py update <old city name> <new city name>")
        else:
            old_city_name = sys.argv[2]
            new_city_name = sys.argv[3]
            update_favorite(old_city_name, new_city_name)

    elif command == "remove":
        if len(sys.argv) < 3:
            print("Usage: weather.py remove <city>")
        else:
            city_to_remove = ' '.join(sys.argv[2:])
            remove_favorite(city_to_remove)
    elif command == "list":
        list_favorites()
    elif command == "refresh":
        try:
            refresh_interval = int(30)
            auto_refresh(refresh_interval)
        except ValueError:
            print("Error: Invalid interval. Please provide an integer value.")
    else:
        print("Invalid command. Available commands: check, add, remove, list, refresh, update")
