import requests

def fetchWolframData(query):
    '''
        This method constructs the Wolfram Alpha API URL, issues an HTTP request to get the webpage and gets Response
        object. From the Response object, it decodes and returns the JSON data.
    '''
    base_wolfram_url = 'http://api.wolframalpha.com/v2/query?'
    wolfram_api_key = 'VK9RKX-V2VJW282RE'

    build_wolfram_url = base_wolfram_url + 'appid=' + wolfram_api_key + '&input=' + query + '&output=json'

    return requests.get(build_wolfram_url).json()

def outputWolframData(data):
    '''
        This method pulls out all the necessary data from the previously obtained json data and returns a resulting string.
    '''
    for pod in data['queryresult']['pods']:
        if pod['title'] == 'Result' or pod['title'] == 'Solution':
            return pod['subpods'][0]['img']['alt']