from asyncore import read
from heapq import merge
import json 
from datetime import datetime
from get_sensor_data import write_data

def process_data():
        

    # open dmi measurements
    with open('../dmi_data/dmi_filtered_data.json', 'r') as f:
        climates = json.loads(f.read())
        print(len(climates))

    # open files devices
    with open('../sensor_data/aarhus-devices.json', 'r') as f:
        devices = json.loads(f.read())

    # open file ship schedule
    with open('../ship/schedule.json', 'r') as f:
        schedules = json.loads(f.read())

    # open PM2.5 measurements
    with open('../sensor_data/latest.json', 'r') as f:
        measurements = json.loads(f.read())
        
    merged_data = []
    num_days_ships = 0
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
        num_days_ships += 1

    print("---------number of days that ships in town:", num_days_ships)

    merged_data = []

    for measurement in measurements:
        for device in devices:
            if measurement['location'] == device['location']:
                local_time_measurement = datetime.strptime(measurement['local_time'], '%H:%M:%S').time().hour
                merged_data.append(
                    {
                        **device,
                        'local_date': measurement['local_date'],
                        'local_time':local_time_measurement,    
                        'mean_P1': measurement["mean_mP1" if "mean_mP1" in measurement else "mean_p1"],
                        'mean_P25': measurement["mean_mP2" if "mean_mP2" in measurement else "mean_p2"]    
                    }
                )
                break

    print("---------number of days that have PM2.5 measurements:", len(measurements))
    print(len(merged_data))

    merged_data2 = []
    numday_climate_data = 0

    for climate in climates:
        for d in merged_data:
            if d['local_date'] == climate['local_date']:
                if d['local_time'] == int(climate['local_time']):
                    merged_data2.append(
                        {
                            **climate,
                            **d,
                        }
                    )
                    break
            numday_climate_data += 1

    print("---------numday_climate_data:", len(climates))
    print(len(merged_data2))


    merged_data3 = []
    total_dataset = 0

    for md in merged_data2:
        # print(md)
        ships = []
        for s in schedules:

            ship_date = datetime.strptime(s['date'], '%Y-%m-%d').date()
            # print(md)
            sensor_date = datetime.strptime(md['local_date'], '%Y-%m-%d').date()    
            if ship_date == sensor_date:
                # print(md['local_time'])
                sensor_hour = md['local_time']
                if sensor_hour in s['time_range']:
                    ships.append(s)
        if len(ships) == 0:
            merged_data3.append({**md, "ship": 0})
        else:
            merged_data3.append({**md, "ship": 1, "ships": ships})

        total_dataset +=1

    print("---------number of row of of the dataset:", len(merged_data3))


    # only run if need to see an intermediate data
    write_data("../dmi_data/dmi_ship_measurements.json", merged_data3)
    return merged_data3

def build_dataset(merged_data):
        
    missing_count =0
    total =0
    for m in merged_data:
        total = total +1
        if "mean_P25" in m:
            pass
        else:
            missing_count = missing_count + 1
    print(total)
    print(missing_count)

    dataset_x = []
    dataset_y = []
    count = [0,0,0,0,0,0]
    vals = []
    for m in merged_data:
        if 'mean_P25' not in m:
            continue
        # to be able to compare value in the standard of 24 hours level
        val = m['mean_P25'] * 24
        catagory = 0

        if val > 10:
            category = 1
        if val >= 20:
            category = 2
        if val >= 25:
            category = 3
        if val >= 50:
            category = 4
        if val >= 75:
            category = 5
        count[category] += 1
        vals.append(val)
    


        dataset_y.append(
                [1 if category == i else 0 for i in range(6)]
        )
        # dataset_y.append(
        #         [val / 24]
        # )
        dataset_x.append(
            [
                m['bright_sunshine'],
                m['max_wind_speed_10min'],
                m['mean_wind_dir'],
                m['mean_temp'],
                m['mean_pressure'],
                m['mean_temp'],
                m['mean_radiation'],
                m['acc_precip'],
                m['mean_cloud_cover'],
                m['mean_wind_speed'],
                len(m['ships']) if m['ship'] == 1 else 0,
                sum(s['Antal Pax'] for s in m['ships']) if m['ship'] == 1 else 0,
                sum(s['Antal crew'] for s in m['ships']) if m['ship'] == 1 else 0,
                sum(len(s['time_range']) for s in m['ships']) if m['ship'] == 1 else 0,
                datetime(*[int(s) for s in m["local_date"].split("-")]).weekday(),
                datetime.strptime(m['local_date'], '%Y-%m-%d').month,
                datetime.strptime(m['local_date'], '%Y-%m-%d').day,
                m['local_time']
                # val /24
            ]
        )
    print(count)

    write_data("../dataset/larger/dataset_x.json", dataset_x)
    write_data("../dataset/larger/dataset_y.json", dataset_y)

if __name__ == "__main__":
    ## if the intermediate data has not been generated
    # merged_data = process_data()

    # else use the generated data 
    # open merged dmi measurements

    with open('../dmi_data/dmi_ship_measurements.json', 'r') as f:
        merged_data = json.loads(f.read())
        print(len(merged_data))

    build_dataset(merged_data)