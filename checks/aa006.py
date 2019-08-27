#!/usr/bin/env python
from checks.check import Check


class AA006(Check):

    ecode: str = "E_MISSING_TIMESERIES"
    desc: str = "Some of the time series in this signalflow don't exist"
    help: str = ""

    def process(self, detector, events, incidents, computation):

        if computation.find_matched_no_timeseries:
            return True

        return False
