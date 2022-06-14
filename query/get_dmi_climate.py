import requests
import json

import datetime
#from zoneinfo import ZoneInfo

from query.dmi_token import token

def write_data(file, response):
    with open(file, "w", encoding='utf8') as f:
        json.dump(response, f, ensure_ascii=False)

def get_climate_data(start, end,  lon1,lat1,lon2,lat2, parameterId, timeResolution): 

    url = "https://dmigw.govcloud.dk/v2/climateData/collections/stationValue/items"

    querystring = {
        "api-key": token,
        "datetime": start + "/" + end,
        "bbox": lon1 + "," + lat1+ "," +  lon2+ "," +  lat2,
        "parameterId": parameterId,
        "timeResolution":timeResolution
    }
    payload = {}

    response = requests.request("GET", url, data=payload, params=querystring)
    return response.json()

def get_devices():

    # open all the devices file
    with open('all-devices.json', 'r') as f:
        data = json.loads(f.read())

    devices = [d for d in data if d['city'].lower().find('aarhus') >= 0]
    write_data('aarhus-devices.json', devices)  

    return devices

if __name__ == '__main__':
    
    start = "2022-04-29T00:00:00+02:00"
    end = "2022-05-23T23:59:59+02:00"


    # lon1 = "7"
    # lat1 = "54"
    # lon2 = "16"
    # lat2 = "58"


    lon1 = "9"
    lat1 = "55"
    lon2 = "11"
    lat2 = "57"
    parameterId = "mean_wind_speed"
    timeResolution="hour"

    # run this if the file has never been generated
    response = []
    response = get_climate_data(start, end,  lon1,lat1,lon2,lat2, parameterId, timeResolution)

    response
    
    # # else this
    # with open('aarhus-devices.json', 'r') as f:
    #     a_devices = json.loads(f.read())

    # location_list = [d['location'] for d in a_devices]
    # response = []

    # for location in location_list:
    #     r = get_sensor_data(start, end, resolution, location)
        
    #     # loop over each response to tranform the time to local time
    #     for i in r: 
    #         #  transform ISPO8601 time to UTC time format, then from UTC to local time
    #         local_dt = datetime.datetime.strptime(i['time'], '%Y-%m-%dT%H:%M:%S.%f%z').astimezone(ZoneInfo('Europe/Copenhagen'))

    #         i['local_date'] = str(local_dt.date())
    #         i['local_time'] = str(local_dt.time())

    #     response += r
    
    write_data("all_dmi_stations.json", response)


