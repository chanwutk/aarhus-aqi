from datetime import datetime
import os
import json
import pytz

def read_filter_write(year):
    
    data = {}
    count = 0
    for filename in os.listdir("../dmi_data/" + year):
        # if count > 10: break
        print(filename, count)
        with open(os.path.join("../dmi_data/" + year, filename), 'r') as f:
            for line in f.readlines():
                d = json.loads(line)
                if d["properties"]["municipalityName"] == 'Aarhus':
                    _from = d["properties"]["from"]
                    __from = datetime.fromisoformat(_from)
                    local_date = str(__from.astimezone(pytz.timezone('Europe/Copenhagen')).date())
                    local_time = str(__from.astimezone(pytz.timezone('Europe/Copenhagen')).time().hour)
                    key = json.dumps([d["geometry"]["coordinates"], local_date, local_time, d["properties"]["municipalityName"]])
                    if key not in data:
                        data[key] = []
                    data[key].append(d)
        count += 1
    
    data2 = []
    for k in data:
        coordinates, local_date, local_time, munacipalityName = json.loads(k)

        datum = {
            "coordinates": coordinates,
            "local_date": str(local_date),
            "local_time": str(local_time),
            "munacipalityName": munacipalityName
        }
        for d in data[k]:
            paramId = d["properties"]["parameterId"]
            datum[paramId] = d["properties"]["value"]
        data2.append(datum)

    return [
        d
        for d in sorted(data2, key=lambda d: (d["local_date"], d["local_time"]))
        if "mean_wind_speed" in d and 
            "acc_precip" in d and 
            "mean_wind_dir" in d and 
            "bright_sunshine" in d
    ]
                

data = [*read_filter_write("2021"), *read_filter_write("2022")]
with open("../dmi_data/dmi_filted_data.json", "w") as f:
    json.dump(data, f)