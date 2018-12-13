import urllib
import json

def fetchMapData(instructions):
    '''
        This method constructs the MapQuest URL, issues an HTTP request to build the URL and gets an HTTP response.
        From the HTTP response, a Python object representing the parsed JSON response is returned.
    '''
    base_mapquest_url = 'http://open.mapquestapi.com'
    mapquest_api_key = 'Fmjtd|luu821ubn0,2s=o5-94ag5w'

    locations = instructions.split('\n')
    query_parameters = [ ('key', mapquest_api_key), ('from', locations[0]) ]
    for l in locations[1:]:
        query_parameters.append(('to', l))

    build_mapquest_url = base_mapquest_url + '/directions/v2/route?' + urllib.parse.urlencode(query_parameters)

    response = urllib.request.urlopen(build_mapquest_url)
    json_text = response.read().decode(encoding='utf-8')
    response.close()

    return json.loads(json_text)

def outputMapData(data):
    '''
        This method pulls out all the necessary data from the previously obtained json data and returns a formatted string.
    '''
    steps = 'DIRECTIONS\n'
    for item in data['route']['legs']:
        for x in item['maneuvers']:
            steps += x['narrative'] + '\n'

    total_distance = 'TOTAL DISTANCE: ' + str(round(data['route']['distance'])) + ' miles.'

    total_time = 'TOTAL TIME: ' + str(round(int(data['route']['time']) / 60)) + ' minutes.'

    lat_long = 'LATLONGS\n'
    for item in data['route']['locations']:   
        lat = item['latLng']['lat']
        if lat > 0:
            latitude = 'N '
        else:
            latitude = 'S '

        long = item['latLng']['lng']
        if long < 0:
            longitude = 'W'
        else:
            longitude = 'E'
        
        lat_long += str("{0:.2f}".format(abs(lat))) + latitude + str("{0:.2f}".format(abs(long))) + longitude + '\n'

    answer = steps + '\n' + total_distance + '\n\n' + total_time + '\n\n' + lat_long
    return answer