import requests

 

url = "https://api.cityflow.live/measurements/history/location/252"

 

querystring = {"from":"2022-04-30T00:00:00.000Z","to":"2022-05-23T23:59:59.999Z"}

 

payload = ""

headers = {'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NTI0LCJpYXQiOjE2MTk2MzAwMzMsImV4cCI6MTkwOTcxNjQzM30.o2XZJEE9RE71Z-2z8oYLYD-9QANbi-fF1iTRvroTrx0'}

 

response = requests.request("GET", url, data=payload, headers=headers, params=querystring)

 

print(response.text)