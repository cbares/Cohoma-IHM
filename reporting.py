#!python
import sched, time

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

DELTA = 1 # seconde

SERVER= "127.0.0.1"
PORT = "8000"
URI = "api/waypoint/reporting"
header = {'accept': 'application/json'}
URL_IHM = f"http://{SERVER}:{PORT}/{URI}"


def update_data_ODAC():
    result = requests.get(URL_IHM, header)
    marker = result.json()

    for m in marker:
        m["team"] = team
        m["auth"] = auth
        r = requests.post(ODAC, json=m)
        if r.status_code != requests.codes.ok:
            print(r.status_code, m)


def schedule_udpate_data(scheduler):
    scheduler.enter(delay=DELTA, priority=1, action=schedule_udpate_data, argument=(scheduler,))
    update_data_ODAC()


cohoma_scheduler = sched.scheduler(time.time, time.sleep)
schedule_udpate_data(cohoma_scheduler)
cohoma_scheduler.run()