import random
import json

SEED = "11111!"
WEATHER_DATA = "weather.json"

dice = random.Random(SEED)
weather_data = json.load(open(WEATHER_DATA))

class Weather():
    def __init__(self, name=None, effects=None, calming1=None, worsening1=None, worsening2=None, duration=None, roll = None):
        self.name = name
        self.effects = effects
        self.calming1 = calming1
        self.worsening1 = worsening1
        self.worsening2 = worsening2
        self.duration = duration
        self.roll = roll

def populate_weather_object(current_weather_object, previous_weather_roll):
    current_weather_object.name = weather_data["weather"][str(previous_weather_roll)]["name"]
    current_weather_object.effects = weather_data["weather"][str(previous_weather_roll)]["effects"]
    current_weather_object.calming1 = weather_data["weather"][str(previous_weather_roll)]["calming1"]
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
    print(f"Status roll result = {str(roll_result)}")
    
    if roll_result <= 50:
        weather_status = "calming1"
        print("Getting Better...")
        print("")
    elif roll_result <=75:
        weather_status = "worsening1"
        print("Getting Worse...")
        print("")
    elif roll_result <= 100:
        weather_status = "worsening2"
        print("Getting Even Worse...")
        print("")
        
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
    print(f"Effects: {str(weather.effects)}")

def weather_sample():
    current_weather = long_rest()
    print_weather(current_weather)
    print("------------")
    
    new_weather = next_weather(current_weather)
    print_weather(new_weather)
    print("------------")
    
    even_newer = next_weather(new_weather)
    print_weather(even_newer)



weather_now = long_rest()

for x in range(10):
    print_weather(weather_now)
    print("--------------------------")
    weather_now = next_weather(weather_now)

