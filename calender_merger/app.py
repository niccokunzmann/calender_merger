from bottle import route, run, template, redirect, static_file, request, \
    SimpleTemplate, response
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
CALENDER_START = 'BEGIN:VCALENDAR\r\nVERSION:2.0\r\nCALSCALE:GREGORIAN\r\nMETHOD:PUBLISH\r\n'
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
    try:
        calender_result = requests.get(url)
    except requests.exceptions.MissingSchema:
        return []
    print("extract_ics {} {}".format(calender_result.status_code, url))
    events = EXTRACT_EVENTS.findall(calender_result.text)
    return events

    
@route('/join-calenders.ics')
def join_calenders():
    set_JS_headers()
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        event_lists = executor.map(extract_ics, request.query.items())
    result = []
    for event_list in event_lists:
        result.extend(event_list)
    result.insert(0, CALENDER_START)
    result.append(CALENDER_END)
    return "".join(result)

def set_JS_headers():
    """Set the response headers for a valid CORS request."""
    response.headers['Access-Control-Allow-Origin'] = '*'
    # see https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS/Errors/CORSMissingAllowHeaderFromPreflight
    response.headers['Access-Control-Allow-Headers'] = request.headers.get("Access-Control-Request-Headers")
    response.headers['Content-Type'] = 'text/calendar'

@route('/join-calenders.ics', method="OPTIONS")
def join_calenders_options():
    set_JS_headers()
    return None

    
def main(argv = sys.argv):
    if len(argv) > 1:
        port = int(sys.argv[1])
    else:
        port = 8080
    run(host='', port=port, debug=True)

if __name__ == "__main__":
    main()
