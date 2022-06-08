import json 
from datetime import datetime
from get_sensor_data import write_data

# open files devices
with open('aarhus-devices.json', 'r') as f:
    devices = json.loads(f.read())

# open file ship schedule
with open('ship/schedule.json', 'r') as f:
    schedules = json.loads(f.read())

with open('sensor-data.json', 'r') as f:
    measurements = json.loads(f.read())

# modified_schedule = schedules
merged_data = []

for schedule in schedules:
    date_str = schedule['Date of arrival']

    date = datetime.strptime(date_str, '%d.%m.%Y').date()       

    time_range = schedule['Period of time'].split('-')
    t = [int(numeric_string) for numeric_string in time_range]
    t_range = list(range(t[0], t[1]+1))

    from_time = datetime.strptime(time_range[0], '%H').time()
    to_time = datetime.strptime(time_range[1], '%H').time()

    schedule['date'] = str(date)
    schedule['from_time'] = str(from_time)
    schedule['to_time'] = str(to_time)
    schedule['time_range'] = t_range

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

merged_data2 = []
for md in merged_data:
    # print(md)
    ships = []
    for s in schedules:
        ship_date = datetime.strptime(s['date'], '%Y-%m-%d').date()
        # print(md)
        sensor_date = datetime.strptime(md['local_date'], '%Y-%m-%d').date()    
        if ship_date == sensor_date:
            sensor_hour = datetime.strptime(md['local_time'], '%H:%M:%S').time()
            if sensor_hour.hour in s['time_range']:
                ships.append(s)
    if len(ships) == 0:
        merged_data2.append({**md, "ship": 0})
    else:
        merged_data2.append({**md, "ship": 1, "ships": ships})

 
write_data("sensor_measurement_schedule.json", merged_data2)