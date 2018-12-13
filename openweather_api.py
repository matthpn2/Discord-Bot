import urllib
import datetime
import json

def fetchWeatherData(cityname):
    '''
        This method constructs the Open Weather Map URL, issues an HTTP request to build the URL and gets an HTTP response.
        From the HTTP response, a Python object representing the parsed JSON response is returned.
    '''
    base_weather_url = 'http://api.openweathermap.org/data/2.5/weather?q='
    weather_api_key = '70eaba6802492b0faeeff8e0d9a3344d'

    build_weather_url = base_weather_url + str(cityname) + '&mode=json&units=imperial&appid=' + weather_api_key

    response = urllib.request.urlopen(build_weather_url)
    json_text = response.read().decode(encoding='utf-8')
    response.close()
    return json.loads(json_text)

def convertTime(time):
    '''
        This method gets the local date corresponding to the POSIX timestamp and converts it to the proper format of 
        "Hour:Minute [AM/PM]", where Hour and Minute are zero-padded decimal numbers.
    '''    
    return datetime.datetime.fromtimestamp(int(time)).strftime('%I:%M %p')

def outputWeatherData(data):
    '''
        This method pulls out all the necessary data from the previously obtained json data and returns a formatted string.
    '''
    cityname = data.get('name')
    country = data.get('sys').get('country')

    current_temp = str(data.get('main').get('temp'))
    sky_desc = data['weather'][0]['main']

    max_temp = str(data.get('main').get('temp_max'))
    min_temp = str(data.get('main').get('temp_min'))

    wind_speed = str(data.get('wind').get('speed'))
    wind_deg = data.get('deg')

    humidity = str(data.get('main').get('humidity'))
    cloudiness = str(data.get('clouds').get('all'))
    pressure = str(data.get('main').get('pressure'))

    sunrise = str(convertTime(data.get('sys').get('sunrise')))
    sunset = str(convertTime(data.get('sys').get('sunset')))
    latest_time = str(convertTime(data.get('dt')))

    temp_symbol = '\xb0' + 'F '

    answer = ( 'Current weather in {}, {}:'.format(cityname, country) + '\n' +  
               current_temp + temp_symbol + sky_desc + ' Skies\n' + 
               'Max Temp: {} {} \nMin Temp: {} {}'.format(max_temp, temp_symbol, min_temp, temp_symbol) + '\n\n' +
               'Wind Speed: {}, Degree: {}'.format(wind_speed, wind_deg) + '\n' +
               'Humidity: {}'.format(humidity) + '\n' +
               'Cloudiness: {}'.format(cloudiness) + '\n' +
               'Pressure: {}'.format(pressure) + '\n' +
               'Sunrise at {}'.format(sunrise) + '\n' +
               'Sunset at {}'.format(sunset) + '\n\n' +
               'Last update from server at {}'.format(latest_time) )
    return answer