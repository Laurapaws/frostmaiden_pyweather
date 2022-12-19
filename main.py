import random
import json
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter

SEED = "boop!"
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

def populate_weather_object(current_weather_object, weather_roll):
    """Populates a weather object with data from WEATHER_DATA

    Args:
        current_weather_object (Weather Object): The current blank weather object 
        previous_weather_roll (int): The dice roll/JSON value of the weather to populate with

    Returns:
        Weather Object: The fully populated weather object from the selected JSON in WEATHER_DATA
    """
    current_weather_object.name = weather_data["weather"][str(weather_roll)]["name"]
    current_weather_object.effects = weather_data["weather"][str(weather_roll)]["effects"]
    current_weather_object.calming1 = weather_data["weather"][str(weather_roll)]["calming1"]
    current_weather_object.calming2 = weather_data["weather"][str(weather_roll)]["calming2"]
    current_weather_object.worsening1 = weather_data["weather"][str(weather_roll)]["worsening1"]
    current_weather_object.worsening2 = weather_data["weather"][str(weather_roll)]["worsening2"]
    current_weather_object.roll = weather_data["weather"][str(weather_roll)]["roll"]
    length_dice = weather_data["weather"][str(weather_roll)]["lengthdice"]
    length_dice_count = weather_data["weather"][str(weather_roll)]["lengthcount"]
    current_weather_object.duration = roll(length_dice_count, length_dice)
    return current_weather_object

def roll(dice_count, max_dice_value):
    """Rolls any number of dice of a single type.

    Args:
        dice_count (int): The amount of dice the roll
        max_dice_value (int): The max value on the face of the die (such as 20)

    Returns:
        int: The result of the dice rolle
    """
    total = 0
    for x in range(dice_count):
        total = total + dice.randint(1, max_dice_value)
    return total

def long_rest():
    """Initial weather roll meant to occur after a long rest. Can just be used as the start of a day.

    Returns:
        Weather Object: Returns a weather object containing weather name, effects (list), calming1, calming2, worsening1, worsening2, weather duration, and the roll value for that weather
    """
    
    weather_roll = roll(1,12)
    print(f"Weather Roll = {str(weather_roll)}")

    current_weather = Weather()
    current_weather = populate_weather_object(current_weather, weather_roll)
    
    return current_weather

def weather_status():
    """Works out whether the net set of weather should be calm or worse (as per WEATHER_DATA)

    Returns:
        str: A string of calming1, calming2, worsening1, or worsening2
    """
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
    """Takes a weather object and works out the next coming weather.

    Args:
        weather (Weather Object): A populated weather object

    Returns:
        Weather Object: A new weather object for the next set of weather
    """
    next_weather_name = getattr(weather, weather_status())
    
    for weather_type in weather_data["weather"].items():
        if weather_type[1]["name"] == next_weather_name:
            new_weather = Weather()
            new_weather = populate_weather_object(new_weather, weather_type[1]["roll"])
        
    return new_weather
            
def print_weather(weather):
    """Prints the current weather to the console including name, duration, and effects of the weather.

    Args:
        weather (Weather Object): A populated weather object
    """
    
    print(f"Weather: {weather.name}")
    print(f"Duration: {str(weather.duration)} hours")
    print(f"Effects: ")
    for effect in weather.effects:
        print(effect)

def weather_sample():
    """Creates a sample set of weather as well as two rolls of weather afterwards
    """
    
    current_weather = long_rest()
    print_weather(current_weather)
    print("------------")
    
    new_weather = next_weather(current_weather)
    print_weather(new_weather)
    print("------------")
    
    even_newer = next_weather(new_weather)
    print_weather(even_newer)

def print_stats():
    """A function just for working out stats. Not intended as production code. Uncomment internal functions text_stats() or graph_stats() to use.
    """
    
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

    # graph_stats(weather_list)
    text_stats(weather_list)
    
def calculate_day(day_length):
    long_rest()
    
calculate_day(24)


#print_stats()