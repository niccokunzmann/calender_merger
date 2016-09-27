from bottle import route, run, template, redirect, static_file, request, \
    SimpleTemplate
import sys
import requests
import os
import pprint
from concurrent.futures import ThreadPoolExecutor
import re

HERE = os.path.dirname(__file__)
STATIC_FILES = os.path.join(HERE, "static")
MAX_WORKERS = 100

# see http://bottlepy.org/docs/dev/stpl.html
TEMPLATES = os.path.join(HERE, "templates")
with open(os.path.join(TEMPLATES, "meetups-list.html")) as file:
    LIST_MEETUPS_TEMPLATE = SimpleTemplate(file.read())

EXTRACT_EVENTS = re.compile('\r\n(BEGIN:VEVENT.*?END:VEVENT\r\n)', re.DOTALL)
CALENDER_START = 'BEGIN:VCALENDAR\r\nVERSION:2.0\r\n'
CALENDER_END = 'END:VCALENDAR\r\n'

@route('/')
def index():
    return redirect("/static/index.html")

@route('/static/<filename>')
def static(filename):
    return static_file(filename, root=STATIC_FILES)
    
@route('/choose-groups')
def choose_groups():
    api_key = request.query.getunicode("api-key")
    if api_key is None:
        return "I need a field 'api-key'!"
    # see https://secure.meetup.com/meetup_api/console/?path=/self/groups
    meetups_url = "https://api.meetup.com/self/groups?key={}".format(api_key)
    meetups = requests.get(meetups_url).json()
    return LIST_MEETUPS_TEMPLATE.render(meetups = meetups)

def extract_ics(argument):
    url, _ = argument
    calender_result = requests.get(url)
    print("extract_ics {} {}".format(calender_result.status_code, url))
    events = EXTRACT_EVENTS.findall(calender_result.text)
    return events

    
@route('/join-calenders.ics')
def join_calenders():
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        event_lists = executor.map(extract_ics, request.query.items())
    result = []
    for event_list in event_lists:
        result.extend(event_list)
    result.insert(0, CALENDER_START)
    result.append(CALENDER_END)
    return "".join(result)
    
def main(argv = sys.argv):
    if len(argv) > 1:
        port = int(sys.argv[1])
    else:
        port = 8080
    run(host='', port=port, debug=True)

if __name__ == "__main__":
    main()