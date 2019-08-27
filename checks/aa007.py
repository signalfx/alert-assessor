#!/usr/bin/env python
from checks.check import Check


class AA008(Check):

    ecode: str = "E_TOOMANY_TIMESERIES"
    desc: str = "Too many time series!"
    help: str = ""

    def process(self, detector, events, incidents, computation):

        if computation.find_limited_resultset:
            return True

        return False
