#!/usr/bin/env python
from checks.check import Check, RuleCheck

class AA015(RuleCheck):

    ecode: str = "E_RULE_MISSING_PARAMETERIZED_BODY"
    desc: str = "No parameterized body"
    help: str = "Adding parameterized subjects allows an alert responder to more quickly understand the context of an alert, consider adding."

    def process(self, detector, events, incidents, computation):

        output = {}

        for i in range(len(detector["rules"])):
            rule = detector["rules"][i]

            if (
                "parameterizedBody" not in rule
                or not rule["parameterizedBody"]
            ):
                output[str(i)] = self.ecode

        return output
