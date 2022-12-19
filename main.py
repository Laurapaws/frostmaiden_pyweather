import random
import json
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter

SEED = "cheesey"
WEATHER_DATA = "weather.json"

dice = random.Random(SEED)
weather_data = json.load(open(WEATHER_DATA))

class Weather():
    def __init__(self, name=None, effects=None, calming1=None, calming2=None, worsening1=None, worsening2=None, duration=None, roll=None):
        self.name = name
        self.effects = effects
        self.calming1 = calming1
        self.calming2 = calming2
        self.worsening1 = worsening1
        self.worsening2 = worsening2
        self.duration = duration
        self.roll = roll

def populate_weather_object(current_weather_object, previous_weather_roll):
    current_weather_object.name = weather_data["weather"][str(previous_weather_roll)]["name"]
    current_weather_object.effects = weather_data["weather"][str(previous_weather_roll)]["effects"]
    current_weather_object.calming1 = weather_data["weather"][str(previous_weather_roll)]["calming1"]
    current_weather_object.calming2 = weather_data["weather"][str(previous_weather_roll)]["calming2"]
    current_weather_object.worsening1 = weather_data["weather"][str(previous_weather_roll)]["worsening1"]
    current_weather_object.worsening2 = weather_data["weather"][str(previous_weather_roll)]["worsening2"]
    current_weather_object.roll = weather_data["weather"][str(previous_weather_roll)]["roll"]
    length_dice = weather_data["weather"][str(previous_weather_roll)]["lengthdice"]
    length_dice_count = weather_data["weather"][str(previous_weather_roll)]["lengthcount"]
    current_weather_object.duration = roll(length_dice_count, length_dice)
    return current_weather_object

def roll(dice_count, max_dice_value):
    
    total = 0
    for x in range(dice_count):
        total = total + dice.randint(1, max_dice_value)
    return total

def long_rest():
    
    weather_roll = roll(1,12)
    print(f"Weather Roll = {str(weather_roll)}")

    current_weather = Weather()
    current_weather = populate_weather_object(current_weather, weather_roll)
    
    return current_weather

def weather_status():
    
    weather_status = "Error weather not calculated"
    roll_result = roll(1,100)
    
    if roll_result <= 25:
        weather_status = "calming1"
    if roll_result <= 50:
        weather_status = "calming2"
    elif roll_result <=75:
        weather_status = "worsening1"
    elif roll_result <= 100:
        weather_status = "worsening2"

        
    return weather_status

def next_weather(weather):
    
    next_weather_name = getattr(weather, weather_status())
    
    for weather_type in weather_data["weather"].items():
        if weather_type[1]["name"] == next_weather_name:
            new_weather = Weather()
            new_weather = populate_weather_object(new_weather, weather_type[1]["roll"])
        
    return new_weather
            
def print_weather(weather):
    print(f"Weather: {weather.name}")
    print(f"Duration: {str(weather.duration)} hours")
    print(f"Effects: ")
    for effect in weather.effects:
        print(effect)

def weather_sample():
    current_weather = long_rest()
    print_weather(current_weather)
    print("------------")
    
    new_weather = next_weather(current_weather)
    print_weather(new_weather)
    print("------------")
    
    even_newer = next_weather(new_weather)
    print_weather(even_newer)

def print_stats():
    # A little function for investigating the weather stats
    
    weather_list = []
    weather_now = long_rest()
    runs = 10000
    print(f"{runs} iterations")

    for x in range(runs):
        #print_weather(weather_now)
        #print("--------------------------")
        weather_list.append(weather_now.name)
        weather_now = next_weather(weather_now)

    def text_stats(weather_list):
        c = Counter(weather_list)
        a = c.keys() 
        b = c.values() 
        for dict_item in c:
            stat = 100 * (c[dict_item] / runs)
            stat = round(stat, 1)
            print(f"{dict_item}: {stat}%")

    def graph_stats(weather_list):
        weather_list_unique = list(set(weather_list))
        counts = [weather_list.count(value) for value in weather_list_unique]
        barcontainer = plt.bar(range(len(weather_list_unique)),counts)
        plt.bar_label(barcontainer,weather_list_unique, label_type='edge')
        plt.axis('off')
        plt.show()

    text_stats(weather_list)
    # graph_stats(weather_list)

# weather_sample()

print_stats()