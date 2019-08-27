#!/usr/bin/env python
from checks.check import Check


class AA004(Check):

    ecode: str = "E_TOO_QUIET"
    desc: str = "Hasn't fired in a while, still working"
    help: str = ""

    def process(self, detector, events, incidents, computation):

        # use DetectLabel to align these TKTK
        if len(incidents) > 0:
            return True

        return False
