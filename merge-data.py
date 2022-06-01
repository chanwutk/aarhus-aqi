import json 
import datetime
from get_sensor_data import write_data

# open files
with open('aarhus-devices.json', 'r') as f:
    devices = json.loads(f.read())

with open('sensor-data.json', 'r') as f:
    measurements = json.loads(f.read())

merged_data = []

for measurement in measurements:
    for device in devices:
        if measurement['location'] == device['location']:
            merged_data.append(
                {
                    **measurement,
                    **device
                }
            )
            break

write_data("sensor_measurement.json", merged_data)