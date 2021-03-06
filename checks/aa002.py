#!/usr/bin/env python
from checks.check import Check
import time

class AA002(Check):

    ecode: str = "E_OLD_BUT_NO_EVENTS"
    desc: str = "hasn't fired, does it work?"
    #TKTK Fix that this message is hardcoded
    help: str = "This alert not fired in the last 30 days, test it to see if it still works."
    config: dict = {"COND_DET_OLD_ENOUGH_FOR_EVENTS_DAYS": 30}

    def process(self, detector, events, incidents, computation):
        age = int(round(time.time() * 1000)) - detector["lastUpdated"]
        if (
            age > self.config["COND_DET_OLD_ENOUGH_FOR_EVENTS_DAYS"] * 86400 * 1000
            and len(events) == 0
        ):
            return True

        return False
