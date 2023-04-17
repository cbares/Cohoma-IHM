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
# ODAC = "http://127.0.0.1:8000/dev/trackers"

DELTA = 1 # seconde

SERVER= "127.0.0.1"
PORT = "8000"
URI = "api/waypoint/reporting"
header = {'accept': 'application/json'}
URL_IHM = f"http://{SERVER}:{PORT}/{URI}"


def spinning_cursor():
    while True:
        for cursor in '|/-\\':
            yield cursor

spinner = spinning_cursor()


def update_data_ODAC(s_src, s_dst):
    global spinner
    result = s_src.get(URL_IHM, headers=header)
    marker = result.json()
    c = 0
    for m in marker:
        m["team"] = team
        m["auth"] = auth
        m["timestamp"] = int(time.time() * 1000)
        r = s_dst.post(ODAC, json=m)
        if r.status_code == requests.codes.ok:
            c = c + 1
        else:
            print(r.status_code, m)
        #time.sleep(0.1)
    if c == len(marker):
        print(next(spinner), end='\b', flush=True)
    else:
        print("x", end='', flush=True)


def schedule_udpate_data(scheduler, s_src, s_dst):
    scheduler.enter(delay=DELTA, priority=1, action=schedule_udpate_data, argument=(scheduler, s_src, s_dst))
    update_data_ODAC(s_src, s_dst)


s_odac = requests.Session()
s_theseus = requests.Session()
cohoma_scheduler = sched.scheduler(time.time, time.sleep)
schedule_udpate_data(cohoma_scheduler, s_theseus, s_odac)
cohoma_scheduler.run()