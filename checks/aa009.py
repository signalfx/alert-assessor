#!/usr/bin/env python
from checks.check import Check


class AA009(Check):

    ecode: str = "E_RULE_INCIDENT_TOO_OLD"
    desc: str = "An incident has been open too long."
    help: str = "Having an incident open this long is a bad sign that it is being ignored. Consider removing."

    config: dict = {"COND_INCIDENT_TOO_OLD_MS": 1 * 86400 * 1000}

    def process(self, detector, events, incidents, computation):

        for i in range(len(incidents)):
            if (
                incidents[i]["events"][0]["timestamp"]
                > self.config["COND_INCIDENT_TOO_OLD_MS"]
            ):
                return True

            return False
