# PyWeather

PyWeather is a simple desktop weather application built using Python and PyQt5. It allows users to fetch and display current weather information for a specified location using the Open-Meteo API.

## Features

- **Location Search**: Enter a city or location name to fetch weather data.
- **Current Weather**: Displays the current temperature, cloud cover, and weather condition.
- **Weather Icons**: Visual representation of weather conditions (e.g., sunny, cloudy, rainy).
- **Error Handling**: Displays error messages if the location is not found or if there is an issue fetching weather data.
- **Stylish UI**: A modern, dark-themed user interface with responsive design.

## Usage

1. Launch the application.
2. Enter a city or location name in the input field.
3. Click the "Submit" button to fetch and display the weather information.

## Code Structure

- **main.py**: The main script that initializes and runs the PyWeather application.
- **MainWindow Class**: Handles the UI setup, user input, and weather data display.
- **API Functions**:

    get_location(location_name): Fetches latitude and longitude for a given location.

    get_weather(location_data): Retrieves current weather data using latitude and longitude.

## API Used
PyWeather uses the Open-Meteo API for geocoding and weather data.
