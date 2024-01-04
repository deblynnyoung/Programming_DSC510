# DSC 510-T304
# Week 12
# Programming Term Project Week 12
# Author Deborah Young
# 11/18/2022

#Change #1
#11/22/2022
#Changed everything
#Programming Term Project Week 12+

import requests, json

api_key = '78015cefb4b26e634ba5b9f4065a4199'
zip_url = "http://api.openweathermap.org/geo/1.0/zip?zip="
city_url = "http://api.openweathermap.org/geo/1.0/direct?q="
weather_url = "https://api.openweathermap.org/data/2.5/weather?"


print("Welcome to your weather app!")


# Function to ask the user for their zip code or city. Iterates through to choose zipcode vs city.
# Make the url from city or state - this function is designed to determine which URL to use based on whether the user
# enters a zip or a city.
#Methods of .numeric or .alpha determine which dictionary key/values to use for lat/lon based on which URL (zip or city);

def get_url():
    global mainurl
    global g
    try:
        if location.isnumeric() and len(location) == 5:
            string_location = str(location)
            zip_complete_url = zip_url + string_location + "," + "US&appid" + "&appid=" + api_key
            g = requests.get(zip_complete_url)
            lat = str(g.json()["lat"])
            lon = str(g.json()["lon"])
            mainurl = city_weather(lat, lon)
            return mainurl
        else:
            state_code = input("Enter US state code (ex. OR for Oregon): ")
            city_complete_url = city_url + location + "," + state_code + "," + "US&limit=5&appid=" + api_key
            g = requests.get(city_complete_url)
            lat = str(g.json()[0]["lat"])
            lon = str(g.json()[0]["lon"])
            mainurl = city_weather(lat, lon)
            return mainurl
    except (IndexError, KeyError):
        print("Whoops, looks like you're in outer space!")
        main()

# Function to use the zip code or city name to obtain weather forecast data from OpenWeatherMap.
def city_weather(lat, lon):
    weather_complete_url = weather_url + "lat=" + lat + "&lon=" + lon + "&appid=" + api_key + "&units="
    return weather_complete_url

# Allow the user to choose between Celsius and Fahrenheit and ideally also Kelvin.
def temp_convert():
    global unit
    measure = input("Which temperature measurement would you like to use? Enter 'F', 'C', or 'K' "
                    "(Fahrenheit, Celsius, Kelvin): ")
    if measure.upper() == "F":
        unit = 'imperial'
        return unit
    elif measure.upper() == "C":
        unit = 'metric'
        return unit
    elif measure.upper() == "K":
        unit = 'standard'
        return unit
    else:
        print("*FCK*...")
        temp_convert()
        # break

# Display the weather forecast in a readable format
def prettyprint():
    global temp
    response = requests.get(call_weather())
    OWdict = json.loads(response.text)
    if str(response.status_code) == "200":
        name = OWdict['name']
        min_t = OWdict['main']["temp_min"]
        max_t = OWdict['main']["temp_max"]
        temp = OWdict['main']['temp']
        feels_like = OWdict['main']['feels_like']
        forecast = OWdict['weather'][0]["description"]

        print("\n***********************",
              "\nYour forecast for: ", name,
              "\nThe low today is", str(round(min_t)),
              "\nThe high today is:", str(round(max_t)),
              "\nRight now, it is", str(round(temp)), "and it feels like", str(round(feels_like)),
              "\nThe ambiance today will be:", forecast, "\n***********************\n")
        main()
    else:
        print("There was an error, please try again.")
        main()


#Function to put all of the functions together and make the URL that calls the weather information from OpenWeather
def call_weather():
    global location
    location = input('Enter US city name or zipcode. Enter "x" to exit. ')
    # g = requests.get(get_url(location))
    while True:
        if str(location).lower() == "x":
            print("Thanks for visiting!")
            exit()
        else:
            get_url()
            try:
                temp_convert()
                final_url = mainurl + unit
                return final_url
            except NameError:
                pass

# Define main function
def main():
    prettyprint()

# Call main function
if __name__ == '__main__':
    main()

