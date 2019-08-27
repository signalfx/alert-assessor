#!/usr/bin/env python
from checks.check import Check, RuleCheck


class AA010(RuleCheck):

    ecode: str = "E_RULE_MISSING_RUNBOOK_URL"
    desc: str = ""
    help: str = ""

    def process(self, detector, events, incidents, computation) -> dict:

        output = {}

        for i in range(len(detector["rules"])):
            rule = detector["rules"][i]

            if "runbookUrl" not in rule or not rule["runbookUrl"]:
                output[str(i)] = self.ecode

        return output
