import logging
import os
import re
import sys
import signalfx
import time

if len(sys.argv) < 2:
    sys.exit("Please provide a detector ID")

if 'SFX_AUTH_KEY' not in os.environ:
    sys.exit("Please provide an SFX_AUTH_KEY environment variable")

detector_id = sys.argv[1]
now_ms = int(round(time.time() * 1000))

RE_USES_PARAMETER_VARS = re.compile('\{\{\S*\}\}')

COND_DET_MATURE_MS = 3 * 86400 * 1000
COND_DET_OLD_ENOUGH_FOR_EVENTS_MS = 30 * 86400 * 1000
COND_DET_FREQUENCY_MS = 86400 * 1000
COND_INCIDENT_TOO_OLD_MS = 1 * 86400 * 1000

E_TOO_IMMATURE = "E_TOO_IMMATURE" # not old enough to draw much from
E_OLD_BUT_NO_EVENTS = "E_OLD_BUT_NO_EVENTS" # hasn't fired, does it work?
E_TOO_NOISY = "E_TOO_NOISY" # Fires too often!
E_TOO_QUIET = "E_TOO_QUIET" # Hasn't fired in a while, still working?
E_MISSING_RULES = "E_MISSING_RULES" # No rules!?
E_MISSING_TIMESERIES = "E_MISSING_TIMESERIES" # Some of the time series in this signalflow don't exist
E_TOOMANY_TIMESERIES = "E_TOOMANY_TIMESERIES" # Too many time series!
E_MISSING_AGGREGATION = "E_MISSING_AGGREGATION" # The aggregation terms don't match
E_RULE_INCIDENT_TOO_OLD = "E_RULE_INCIDENT_TOO_OLD" # An incident open this long is a bad sign that it is being ignored
E_RULE_MISSING_RUNBOOK_URL = "E_RULE_MISSING_RUNBOOK_URL"
E_RULE_MISSING_TIP = "E_RULE_MISSING_TIP"
E_RULE_MISSING_NOTIFICATIONS = "E_RULE_MISSING_NOTIFICATIONS"
E_RULE_MISSING_PARAMETERIZED_SUBJECT = "E_RULE_MISSING_PARAMETERIZED_SUBJECT"
E_RULE_NOVARS_PARAMETERIZED_SUBJECT = "E_RULE_NOVARS_PARAMETERIZED_SUBJECT"
E_RULE_MISSING_PARAMETERIZED_BODY = "E_RULE_MISSING_PARAMETERIZED_BODY"
E_RULE_NOVARS_PARAMETERIZED_BODY = "E_RULE_NOVARS_PARAMETERIZED_BODY"

result = {
    'problems': [],
    'rule_problems': []
}

def assess_program(program_text):
    received = 0
    with signalfx.SignalFx().signalflow(os.environ['SFX_AUTH_KEY']) as flow:
        logging.info("Preflighting SignalFlow for diagnosis (may take a few seconds)")
        logging.info(program_text)
        computation = flow.preflight(program_text, now_ms - (3600 * 1000), now_ms)
        for msg in computation.stream():
            pass

        if computation.find_matched_no_timeseries:
            result['problems'].append(E_MISSING_TIMESERIES)
        if computation.find_limited_resultset:
            result['problems'].append(E_TOOMANY_TIMESERIES)
        if computation.group_by_missing_property:
            result['problems'].append(E_MISSING_AGGREGATION)

        computation.close()
        logging.info("Finished execution")

def assess_detector(detector):
    assess_program(detector['programText'])

def assess_rules(detector):
    if 'rules' not in detector or len(detector['rules']) < 1:
        result['problems'].append(E_MISSING_RULES)

    for i in range(len(detector['rules'])):
        rule = detector['rules'][i]
        rule_problems = []
        if 'runbookUrl' not in rule or not rule['runbookUrl']:
            rule_problems.append(E_RULE_MISSING_RUNBOOK_URL)

        if 'tip' not in rule or not rule['tip']:
            rule_problems.append(E_RULE_MISSING_TIP)

        if 'notifications' not in rule or len(rule['notifications']) < 1:
            rule_problems.append(E_RULE_MISSING_NOTIFICATIONS)

        if 'parameterizedSubject' not in rule or not rule['parameterizedSubject']:
            rule_problems.append(E_RULE_MISSING_PARAMETERIZED_SUBJECT)
        else:
            if not RE_USES_PARAMETER_VARS.search(rule['parameterizedSubject']):
                rule_problems.append(E_RULE_NOVARS_PARAMETERIZED_SUBJECT)

        if 'parameterizedBody' not in rule or not rule['parameterizedBody']:
            rule_problems.append(E_RULE_MISSING_PARAMETERIZED_BODY)
        else:
            if not RE_USES_PARAMETER_VARS.search(rule['parameterizedBody']):
                rule_problems.append(E_RULE_NOVARS_PARAMETERIZED_BODY)

        result['rule_problems'].append(rule_problems)

def assess_incidents(detector, incidents):
    # use DetectLabel to align these TKTK
    if len(incidents) > 0:
        # Take this out for clarify. We can't be too quiet if we're fired
        result['problems'].remove(E_TOO_QUIET)
    for i in range(len(incidents)):
        inc = incidents[i]
        began_ts = now_ms = inc['events'][0]['timestamp']
        if began_ts > COND_INCIDENT_TOO_OLD_MS:
            result['problems'].append(E_RULE_INCIDENT_TOO_OLD)

def assess_events(detector, events):
    age = now_ms - detector['lastUpdated']
    if age < COND_DET_MATURE_MS:
        result['problems'].append(E_TOO_IMMATURE)
        return

    print(age)
    if age > COND_DET_OLD_ENOUGH_FOR_EVENTS_MS and len(events) == 0:
        result['problems'].append(E_OLD_BUT_NO_EVENTS)
        return

    event_count = len(events)
    last_ts = None
    occurrences = []
    events = sorted(events, key = lambda e: e['timestamp'])
    for i in range(len(events)):
        ev = events[i]
        ts = ev['timestamp']
        if last_ts is None:
            last_ts = ts
            continue
        occurrences.append(ts - last_ts) # The time between events
        last_ts = ts
    average = reduce(lambda x, y: x + y, occurrences) / event_count
    if average < COND_DET_FREQUENCY_MS:
        result['problems'].append(E_TOO_NOISY)

    if last_ts > COND_DET_OLD_ENOUGH_FOR_EVENTS_MS:
        result['problems'].append(E_TOO_QUIET)

format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

with signalfx.SignalFx().rest(os.environ['SFX_AUTH_KEY']) as sfx:
    det = sfx.get_detector(detector_id)
    if det == None:
        sys.exit("Unable to find detector id {0}".format(detector_id))
    assess_detector(det)
    assess_rules(det)

    events = sfx.get_detector_events(detector_id)
    assess_events(det, events)

    incidents = sfx.get_detector_incidents(detector_id)
    assess_incidents(det, incidents)

print "Results:"
print(result)
