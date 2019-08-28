#!/usr/bin/env python
import re
from checks.check import Check, RuleCheck


class AA014(RuleCheck):

    ecode: str = "E_RULE_NOVARS_PARAMETERIZED_SUBJECT"
    desc: str = "No parameterized subject vars"
    help: str = "Using a parameterized subject with no vars misses out in improved context. Consider adding tags from the alert result."

    def process(self, detector, events, incidents, computation):

        output = {}

        for i in range(len(detector["rules"])):
            rule = detector["rules"][i]

            if not RuleCheck.RE_USES_PARAMETER_VARS.search(
                rule["parameterizedSubject"]
            ):
                output[str(i)] = self.ecode

        return output
