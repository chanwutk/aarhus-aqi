from asyncore import write
import pandas as pd
import json

from query.get_sensor_data import write_data


# open files devices
with open('sensor-data.json', 'r') as f:
    devices = json.loads(f.read())

df = pd.DataFrame(devices)

print('SAMPLE DATA: ')
print(df.sample(10))


print('STATS OF THE DATA: ')
print(df['mean_t'].unique())

print('INFORMATION OF THE DATA: ')
print(df.info())