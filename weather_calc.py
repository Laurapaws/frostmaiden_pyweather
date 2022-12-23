import random
import json
import matplotlib.pyplot as plt
from collections import Counter
import config


#SEED = "platypus"
#WEATHER_DATA = "weather.json"

def init_data_seed(seed: str, data: str):
    """Sets the seed and weather data JSON file.

    Args:
        seed (str): The random seed to use when rolling dice
        data (str): The reference to the weather data JSON

    Returns:
        Random: An instance of the random.Random() class
        dict: An opened up JSON file of your weather
    """
    dice = random.Random(seed)
    weather_data = json.load(open(data))
    
    return dice, weather_data

class Weather():
    """A weather object containing duration, effects, and chance of the next weather.
    """
    def __init__(self, name=None, effects=None, calming1=None, calming2=None, worsening1=None, worsening2=None, duration=None, start_time=None, end_time=None, roll=None):
        self.name = name
        self.effects = effects
        self.calming1 = calming1
        self.calming2 = calming2
        self.worsening1 = worsening1
        self.worsening2 = worsening2
        self.duration = duration
        self.start_time = start_time
        self.end_time = end_time
        self.roll = roll

def populate_weather_object(current_weather_object: Weather, weather_roll: int):
    """Populates a weather object with data from WEATHER_DATA

    Args:
        current_weather_object (Weather Object): The current blank weather object 
        weather_roll (int): The dice roll/JSON value of the weather to populate with

    Returns:
        Weather Object: The fully populated weather object from the selected JSON in WEATHER_DATA
    """
    current_weather_object.name = weather_data["weather"][weather_roll-1]["name"]
    current_weather_object.effects = weather_data["weather"][weather_roll-1]["effects"]
    current_weather_object.calming1 = weather_data["weather"][weather_roll-1]["calming1"]
    current_weather_object.calming2 = weather_data["weather"][weather_roll-1]["calming2"]
    current_weather_object.worsening1 = weather_data["weather"][weather_roll-1]["worsening1"]
    current_weather_object.worsening2 = weather_data["weather"][weather_roll-1]["worsening2"]
    current_weather_object.roll = weather_data["weather"][weather_roll-1]["roll"]
    length_dice = weather_data["weather"][weather_roll-1]["lengthdice"]
    length_dice_count = weather_data["weather"][weather_roll-1]["lengthcount"]
    current_weather_object.duration = roll(length_dice_count, length_dice)
    return current_weather_object

def roll(dice_count: int, max_dice_value: int):
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
    elif roll_result <= 50:
        weather_status = "calming2"
    elif roll_result <=75:
        weather_status = "worsening1"
    elif roll_result <= 100:
        weather_status = "worsening2"

        
    return weather_status

def next_weather(weather: Weather):
    """Takes a weather object and works out the next coming weather.

    Args:
        weather (Weather Object): A populated weather object

    Returns:
        Weather Object: A new weather object for the next set of weather
    """
    next_weather_name = getattr(weather, weather_status())
    
    for weather_type in weather_data["weather"]:
        if weather_type["name"] == next_weather_name:
            new_weather = Weather()
            new_weather = populate_weather_object(new_weather, weather_type["roll"])
        
    return new_weather
            
def print_weather(weather: Weather, effects: bool, clock: bool):
    """Prints the current weather to the console including name, duration, and effects of the weather.

    Args:
        weather (Weather Object): A populated weather object
        effects (bool): True will generate effects in the printout, False will not
        clock (bool): True will generate 24hr times around the clock. False will not
    """
    
    print(f"Weather: {weather.name}")
    print(f"Duration: {str(weather.duration)} hours")
    if clock:
        print(f"{weather.start_time}:00 - {weather.end_time}:00")
    if effects:
        print(f"Effects: ")
        for effect in weather.effects:
            print(effect)
    
def weather_sample():
    """Creates a sample set of weather as well as two rolls of weather afterwards
    """
    
    current_weather = long_rest()
    print_weather(current_weather, True, False)
    print("------------")
    
    new_weather = next_weather(current_weather)
    print_weather(new_weather, True, False)
    print("------------")
    
    even_newer = next_weather(new_weather)
    print_weather(even_newer, True, False)

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
    
def calculate_day(day_length: int):
    """Creates a set of weather objects spanning day_length hours. Checks to make sure the final weather object doesn't go past day_length and shortens if so.

    Args:
        day_length (int): The length of your day in hours

    Returns:
        _type_: A list of weather objects that span day_length hours in duration.
    """
    
    hour_tracker = 0    
    weather_list = []
    
    starting_weather = long_rest()
    weather_list.append(starting_weather)
    hour_tracker = hour_tracker + starting_weather.duration
    
    new_weather = next_weather(starting_weather)
    weather_list.append(new_weather)
    hour_tracker = hour_tracker + new_weather.duration
    
    while hour_tracker < day_length:
        new_weather = next_weather(new_weather)
        
        if (new_weather.duration + hour_tracker) > day_length:
            remainder_duration = day_length - hour_tracker
            new_weather.duration = remainder_duration
        elif hour_tracker == day_length:
            return
            
        weather_list.append(new_weather)
        hour_tracker = hour_tracker + new_weather.duration

    return weather_list

def populate_times(weather_list: list, current_time: int, day_length: int):
    """Sets up the start and end times of each weather.

    Args:
        weather_list (List): A list of Weather objects
        current_time (int): The time of day you want to start at in hours
        day_length (int): The length of the day in hours

    Returns:
        List: A list of Weather objects
    """
        
    weather_list[0].start_time = current_time
    
    if (current_time + weather_list[0].duration) >= day_length:
        weather_list[0].end_time = (weather_list[0].duration - (day_length - current_time))
        current_time = weather_list[0].end_time
    else:
        weather_list[0].end_time = current_time + weather_list[0].duration
        current_time = weather_list[0].end_time
        
    for idx, weather_object in enumerate(weather_list):
        if idx != 0:
            if (current_time + weather_object.duration) >= day_length:
                weather_object.start_time = weather_list[idx-1].end_time
                weather_object.end_time = (weather_object.duration - (day_length - current_time))
                current_time = weather_object.end_time
            else:
                weather_object.start_time = weather_list[idx-1].end_time
                weather_object.end_time = current_time + weather_object.duration
                current_time = weather_object.end_time
    
    return weather_list

dice, weather_data = init_data_seed(config.SEED, config.WEATHER_DATA)