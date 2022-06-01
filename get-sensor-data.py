import requests
import json

from .token import token

def write_data(file, response):
    with open(file, "w") as f:
        f.write(response.text)

def get_sensor_data(start, end): 

    # TODO get the for loop 
    url = "https://api.cityflow.live/measurements/history/location/252"

    querystring = {"from": start,"to": end}

    payload = ""

    #TODO hidden bearer token 
    headers = {'Authorization': token}

    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
    return response

def get_devices_locations():

    # open all the devices file
    f = open('all-devices.json')
    data = json.loads(f)

    # TODO: filter only from Aarhus
    filtered = 

    # close file
    f.close()




if __name__ == '__main__':
    
    start = "2022-04-29T00:00:00.000Z"
    end = "2022-05-23T23:59:59.999Z"

    #response = get_sensor_data(start, end)
    #write_data("sensor-data.json", response)
