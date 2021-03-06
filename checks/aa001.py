#!/usr/bin/env python
from checks.check import Check
import time

class AA001(Check):

    ecode: str = "E_TOO_IMMATURE"
    desc: str = "Not old enough to draw much from"
    help: str = "Let this alert cook a bit longer and try again!"

    config: dict = {"COND_DET_MATURE_MS": 3 * 86400 * 1000}

    def process(self, detector, events, incidents, computation):

        age = int(round(time.time() * 1000)) - detector["lastUpdated"]
        if age < self.config["COND_DET_MATURE_MS"]:
            return True

        return False
