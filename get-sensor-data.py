import requests
import json

def write_data(file, response):
    with open(file, "w") as f:
        f.write(response.text)

def get_sensor_data(start, end): 

    url = "https://api.cityflow.live/measurements/history/location/252"

    querystring = {"from": start,"to": end}

    payload = ""
    headers = {'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NTI0LCJpYXQiOjE2MTk2MzAwMzMsImV4cCI6MTkwOTcxNjQzM30.o2XZJEE9RE71Z-2z8oYLYD-9QANbi-fF1iTRvroTrx0'}

    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
    return response

def get_devices_locations():



if __name__ == '__main__':
    
    start = "2022-04-29T00:00:00.000Z"
    end = "2022-05-23T23:59:59.999Z"

    response = get_sensor_data(start, end)
    write_data("sensor-data.json", response)
