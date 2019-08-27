#!/usr/bin/env python
import re
from checks.check import Check, RuleCheck


class AA013(RuleCheck):

    ecode: str = "E_RULE_MISSING_PARAMETERIZED_SUBJECT"
    desc: str = ""
    help: str = ""

    RE_USES_PARAMETER_VARS = re.compile("\{\{\S*\}\}")

    def process(self, detector, events, incidents, computation):

        output = {}

        for i in range(len(detector["rules"])):
            rule = detector["rules"][i]

            if (
                "parameterizedSubject" not in rule
                or not rule["parameterizedSubject"]
            ):
                output[str(i)] = self.ecode

        return output
