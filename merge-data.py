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

 
# write_data("sensor_measurement_schedule.json", merged_data2)
missing_count =0
total =0
for m in merged_data2:
    total = total +1
    if "mean_mP2" in m:
        pass
    else:
        missing_count = missing_count + 1
print(total)
print(missing_count)

dataset_x = []
dataset_y = []
for m in merged_data2:
    dataset_y.append(
        [
            m["mean_mP2" if "mean_mP2" in m else "mean_p2"]
        ]
    )
    dataset_x.append(
        [
            # # TODO add rain min/max, #particles
            # m["latitude"],
            # m["longitude"],
            m["mean_l"],
            m["mean_p"],
            m["mean_rA" if "mean_rA" in m else "mean_r.avg"] ,
            # m["mean_t"],
            len(m['ships']) if m['ship'] == 1 else 0,
            sum(s['Antal Pax'] for s in m['ships']) if m['ship'] == 1 else 0,
            sum(s['Antal crew'] for s in m['ships']) if m['ship'] == 1 else 0,
            sum(len(s['time_range']) for s in m['ships']) if m['ship'] == 1 else 0,
            datetime(*[int(s) for s in m["local_date"].split("-")]).weekday(),
            # datetime.strptime(md['local_date'], '%Y-%m-%d').year,
            datetime.strptime(md['local_date'], '%Y-%m-%d').month,
            datetime.strptime(md['local_date'], '%Y-%m-%d').day,  
            datetime.strptime(m['local_time'], '%H:%M:%S').time().hour,
            m["mean_mP2" if "mean_mP2" in m else "mean_p2"]
        ]
    )

write_data("./dataset/dataset_x.json", dataset_x)
write_data("./dataset/dataset_y.json", dataset_y)