#!/usr/bin/env python
from checks.check import Check, RuleCheck


class AA011(RuleCheck):

    ecode: str = "E_RULE_MISSING_TIP"
    desc: str = ""
    help: str = ""

    def process(self, detector, events, incidents, computation):

        output = {}

        for i in range(len(detector["rules"])):
            rule = detector["rules"][i]

            if "tip" not in rule or not rule["tip"]:
                output[str(i)] = self.ecode

        return output
