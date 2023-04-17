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

SERVER= "127.0.0.1"
PORT = "8000"
URI = "api/waypoint/reporting"
header = {'accept': 'application/json'}

def update_data_ODAC():
    result = requests.get(f"http://{SERVER}:{PORT}/{URI}", header)
    marker = result.json()

    for m in marker:
        m["team"] = team
        m["auth"] = auth
        r = requests.post(ODAC, json=m)
        if r.status_code != requests.codes.ok:
            print(r.status_code, m)


def do_something(scheduler):
    # schedule the next call first
    scheduler.enter(1, 1, do_something, (scheduler,))
    # then do your stuff:
    print(".",end='')
    update_data_ODAC()


my_scheduler = sched.scheduler(time.time, time.sleep)
my_scheduler.enter(2, 1, do_something, (my_scheduler,))
my_scheduler.run()