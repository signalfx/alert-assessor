#!/usr/bin/env python
from checks.check import Check

class AA008(Check):

    ecode: str = "E_MISSING_AGGREGATION"
    desc: str = "The aggregation terms don't match"
    help: str = "Some of the time series in this alert have mismatched aggregation terms. Check the queries!"

    def process(self, detector, events, incidents, computation):

        if computation.group_by_missing_property:
            return True

        return False
