import requests
import json

import datetime
from zoneinfo import ZoneInfo

from bearer_token import token

def write_data(file, response):
    with open(file, "w", encoding='utf8') as f:
        json.dump(response, f, ensure_ascii=False)

def get_sensor_data(start, end, resolution, location): 

    url = "https://api.cityflow.live/measurements/history/location/" + str(location)

    querystring = {"from": start,"to": end, "resolution": resolution}
    payload = ""

    headers = {'Authorization': token}

    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
    rr = response.json()
    if response.status_code != 200:
        print("error: ", response.status_code, response.reason)
        return []
    # print(rr)
    return [{**r, 'location': location} for r in rr]

def get_devices():

    # # open all the devices file
    # with open('../sensor_data/all-devices.json', 'r') as f:
    #     data = json.loads(f.read())

    # get from url GET https://api.cityflow.live/devices

    url = "https://api.cityflow.live/devices"

    querystring = {"from": start,"to": end, "resolution": resolution}
    payload = ""

    headers = {'Authorization': token}

    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
    data = response.json()

    devices = [d for d in data if d['city'].lower().find('aarhus') >= 0]
    write_data('../sensor_data/aarhus-devices.json', devices)

    return devices

if __name__ == '__main__':
    
    # start = "2022-04-29T00:00:00.000Z"
    start = "2021-01-01T00:00:00.000Z"
    end = "2022-05-23T23:59:59.999Z"
    resolution = "60m"

    ## run this if the device listfile has never been generated
    a_devices = get_devices()
    
    # else this
    # with open('../sensor_data/aarhus-devices.json', 'r') as f:
    #     a_devices = json.loads(f.read())
    # print(a_devices)

    location_list = [d['location'] for d in a_devices]
    response = []

    for location in location_list:
        print(location)

        r = get_sensor_data(start, end, resolution, location)
        
        # loop over each response to tranform the time to local time
        for i in r: 
            #  transform ISPO8601 time to UTC time format, then from UTC to local time
            local_dt = datetime.datetime.strptime(i['time'], '%Y-%m-%dT%H:%M:%S.%f%z').astimezone(ZoneInfo('Europe/Copenhagen'))

            i['local_date'] = str(local_dt.date())
            i['local_time'] = str(local_dt.time())

        response += r
    
    write_data("../sensor_data/latest.json", response)


