import requests
import json

from bearer_token import token

def write_data(file, response):
    with open(file, "w", encoding='utf8') as f:
        json.dump(response, f, ensure_ascii=False)

def get_sensor_data(start, end, location): 

    url = "https://api.cityflow.live/measurements/history/location/" + location

    querystring = {"from": start,"to": end}
    payload = ""

    headers = {'Authorization': token}

    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
    return response

def get_devices():

    # open all the devices file
    with open('all-devices.json', 'r') as f:
        data = json.loads(f.read())

    devices = [d for d in data if d['city'].lower().find('aarhus') >= 0]
    write_data('aarhus-devices.json', devices)

    return devices

if __name__ == '__main__':
    
    start = "2022-04-29T00:00:00.000Z"
    end = "2022-05-23T23:59:59.999Z"
    resolution = "60m"

    devices = get_devices()
    location_list = [d['location'] for d in devices]
    print(location_list)
    response = ""

    

    #write_data("sensor-data.json", response)
