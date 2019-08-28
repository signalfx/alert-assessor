#!/usr/bin/env python
from checks.check import Check


class AA008(Check):

    ecode: str = "E_TOOMANY_TIMESERIES"
    desc: str = "Too many time series!"
    help: str = "The number of time series involved in this query is being limited, consider adding filters or using `partition_filter`."

    def process(self, detector, events, incidents, computation):

        if computation.find_limited_resultset:
            return True

        return False
