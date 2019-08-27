#!/usr/bin/env python
from checks.check import Check, RuleCheck


class AA012(RuleCheck):

    ecode: str = "E_RULE_MISSING_NOTIFICATIONS"
    desc: str = ""
    help: str = ""

    def process(self, detector, events, incidents, computation):

        output = {}

        for i in range(len(detector["rules"])):
            rule = detector["rules"][i]

            if "notifications" not in rule or len(rule["notifications"]) < 1:
                output[str(i)] = self.ecode

        return output
