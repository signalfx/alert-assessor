#!/usr/bin/env python
from checks.check import Check
from functools import reduce

class AA003(Check):

    ecode: str = "E_TOO_NOISY"
    desc: str = "Fires too often!"
    help: "This detector fires an average of once per day, consider adjusting."

    config: dict = {"COND_DET_FREQUENCY_SECONDS": 86400}

    def process(self, detector, events, incidents, computation):

        event_count = len(events)
        if event_count == 0:
            return False
        last_ts = None
        occurrences = []
        events = sorted(events, key=lambda e: e["timestamp"])
        for i in range(len(events)):
            ev = events[i]
            ts = ev["timestamp"]
            if last_ts is None:
                last_ts = ts
                continue
            occurrences.append(ts - last_ts)  # The time between events
            last_ts = ts
        average = reduce(lambda x, y: x + y, occurrences) / event_count

        if average < self.config["COND_DET_FREQUENCY_MS"] * 1000:
            return True

        return False
