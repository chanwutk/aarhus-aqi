import pandas as pd
import json


# open files devices
with open('ship/schedule.json', 'r') as f:
    devices = json.loads(f.read())

df = pd.DataFrame(devices)

print(df.sample(10))
print(df.describe())

print(df.info())