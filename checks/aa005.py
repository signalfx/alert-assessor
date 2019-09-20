#!/usr/bin/env python
from checks.check import Check

class AA005(Check):

    ecode: str = "E_MISSING_RULES"
    desc: str = "No rules!"
    help: str = "This alert has no rules, so it isn't doing anything. Add rules or remove!"

    def process(self, detector, events, incidents, computation):

        if "rules" not in detector or len(detector["rules"]) < 1:
            return True

        return False
