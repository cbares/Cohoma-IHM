#!python

import requests

"""
curl -X 'GET' \
  'http://127.0.0.1:8000/api/waypoint/reporting' \
  -H 'accept: application/json'
"""
team = "theseus"
auth = "5fyg-mqqs-rxqu-sfjm-pl2d"
ODAC = "https://6bus5bof45.execute-api.eu-west-3.amazonaws.com/dev/trackers"
ODAC = "http://127.0.0.1:8000/dev/trackers"

SERVER= "127.0.0.1"
PORT = "8000"
URI = "api/waypoint/reporting"
header = {'accept': 'application/json'}

result = requests.get(f"http://{SERVER}:{PORT}/{URI}", header)
marker = result.json()

for m in marker:
    m["team"] = team
    m["auth"] = auth
    requests.post(ODAC, json=m)

