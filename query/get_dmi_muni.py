import requests
import json
import pandas as pd
#from zoneinfo import ZoneInfo

from dmi_token import token

def write_data(file, response):
    with open(file, "w", encoding='utf8') as f:
        json.dump(response, f, ensure_ascii=False)

def get_climate_data(start, end, municipalityId, timeResolution, limit): 

    url = "https://dmigw.govcloud.dk/v2/climateData/collections/municipalityValue/items"

    querystring = {
        "api-key": token,
        "datetime": start + "/" + end,
        "municipalityId":municipalityId,
        "timeResolution":timeResolution,
        "limit": "limit"
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
    municipalityId = "0751"
    timeResolution="hour"
    limit="300000"

    # run this if the file has never been generated
    response = []
    response = get_climate_data(start, end, municipalityId, timeResolution, limit)
    
    
    # df = pd.DataFrame(response)
    # for i in df['features']:
    #     print('from: ', df['properties']['from'], ' to: ', i['properties']['to'])

    
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
    
    write_data("../dmi_data/all_dmi_aarhus2.json", response)


