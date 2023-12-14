    """This is a script that fetches the current weather data through an API call to Weatherstack. The free subscription allows
    to retrieve current weather conditions (December 2023). It then asks for you input on the clothing choices and saves it into a 
    csv file. 
    """

import requests
import pandas as pd
import csv
from enum import Enum
from datetime import datetime

class JackaScale(Enum):
    short_shorts = 1 # short pants and short sleeves
    shlongs = 2 # short pants, long sleeves - or vice versa
    longs = 3 # long pants, long sleeves, but still no jacket!
    light_jacket = 4 # spring or autumn jacket, alternatively a rain jacket
    heavy_jacket = 5 # winter jacket
    climb_inside_the_carcass_of_a_Tauntaun_to_avoid_freezing_to_death = 6 # let's be friends if you get this reference!

def fetch_weather():
    url = "http://api.weatherstack.com/current"
    key = "..." # to get your own key register for a free subscription at weatherstack.com

    params = {
        "access_key": key,
        "query": "..." # fill in the location, for me worked best with GPS coordinates
    }

    response = requests.get(url, params)

    if response.status_code == 200:
        data = pd.DataFrame(response.json()["current"]).drop("weather_icons", axis=1)
        data["reporting_date"] = datetime.today().strftime("%Y-%m-%d %H:%M")
        data["jacka_status"] = jacka_or_no_jacka()

    else:
        print(f"Error: {response.status_code}")
        print(response.text)

    return data


def jacka_or_no_jacka():
    while True:
        for option in JackaScale:
            print(f"{option.value}: {option.name}")
        choice = input("Type in your choice: ")
        try:
            if int(choice) in [option.value for option in JackaScale]: 
                choice = int(choice)
                print("Your choice is: ", JackaScale(choice).name)
                action = input("Is that correct? y/n")
                if action == "y":
                    return choice
        except TypeError as e:
            print(e)

def save_to_file(row):
    # making sure the order is the same in case changes are made to the API
    data = row[["observation_time","temperature","weather_code","weather_descriptions",
                "wind_speed",  "wind_degree", "wind_dir", "pressure" , "precip" , "humidity",  "cloudcover",
                "feelslike",  "uv_index",  "visibility", "is_day", "reporting_date", "jacka_status"]]
    print(data)
    #data.to_csv("jacka_records.csv", index = False) # run this in case the original file isn't there
    with open("jacka_records.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(data.loc[0])



if __name__ == "__main__":
    save_to_file(fetch_weather())