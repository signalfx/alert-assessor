#!/usr/bin/env python
from checks.check import Check, RuleCheck


class AA016(RuleCheck):

    ecode: str = "E_RULE_NOVARS_PARAMETERIZED_BODY"
    desc: str = ""
    help: str = ""

    def process(self, detector, events, incidents, computation):

        output = {}

        for i in range(len(detector["rules"])):
            rule = detector["rules"][i]

            if not RuleCheck.RE_USES_PARAMETER_VARS.search(
                rule["parameterizedBody"]
            ):
                output[str(i)] = self.ecode

        return output
