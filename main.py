from flask import Flask, render_template
import weather_calc

def main():

    # app = Flask(__name__)

    # @app.route("/")
    # def index():
    #     return "Weather website!"
    
    # app.run(host="0.0.0.0", port=5000)
    
    todays_weather = weather_calc.calculate_day(24)

    todays_weather = weather_calc.populate_times(todays_weather, 9, 24)

    for x in todays_weather:
        print("----------------------")
        weather_calc.print_weather(x,False,True)
        print("")


if __name__ == '__main__':
    main()

