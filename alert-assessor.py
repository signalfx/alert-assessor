#!/usr/bin/env python
import logging
import os
import click
import sys
import json
import time
import requests
import signalfx

from typing import Dict, List

from checks.check import Check, RuleCheck
from checks import *

format = "%(asctime)s: %(message)s"


class Payload:
    detector: dict
    events: list
    incidents: list


@click.command()
@click.option(
    "--sfx_auth_key",
    default=os.getenv("SFX_AUTH_KEY", ""),
    help="SFX token (or SFX_AUTH_KEY env variable)",
)
@click.option(
    "--api_endpoint",
    default="https://api.signalfx.com",
    help="API endpoint",
    show_default=True,
)
@click.option(
    "--stream_endpoint",
    default="https://stream.signalfx.com",
    help="Stream endpoint",
    show_default=True,
)
@click.option(
    "--format",
    default="human",
    type=click.Choice(["human", "json"]),
    help="Output format ('json' disables verbose output)",
    show_default=True,
)
@click.option("--verbose", is_flag=True, default=False)
@click.argument("detector_id")
def main(
    sfx_auth_key, api_endpoint, stream_endpoint, format, verbose, detector_id
):

    if verbose:
        lvl = logging.DEBUG
    else:
        lvl = logging.INFO

    if format == "json":
        lvl = logging.CRITICAL

    logging.basicConfig(format=format, level=lvl, datefmt="%H:%M:%S")

    with signalfx.SignalFx(
        api_endpoint=api_endpoint, stream_endpoint=stream_endpoint
    ).rest(sfx_auth_key) as sfx:

        try:
            detector = sfx.get_detector(detector_id)
            events = sfx.get_detector_events(detector_id)
            incidents = sfx.get_detector_incidents(detector_id)
        except requests.exceptions.HTTPError as e:
            sys.exit(
                "Unable to find detector id {0} ({1})".format(detector_id, e)
            )

        with signalfx.SignalFx(
            api_endpoint=api_endpoint, stream_endpoint=stream_endpoint
        ).signalflow(sfx_auth_key) as flow:

            computation = flow.preflight(
                detector["programText"],
                int(round(time.time() * 1000)) - (3600 * 1000),
                int(round(time.time() * 1000)),
            )
            for _ in computation.stream():
                pass

            logging.info(
                "Registered %d rule(s)"
                % (
                    len(Check.__subclasses__())
                    + len(RuleCheck.__subclasses__())
                )
            )

            warnings: Dict[str, List] = {}

            for check in Check.__subclasses__():
                logging.debug("Processing %s" % check.ecode)
                ch = check()
                if ch.process(detector, events, incidents, computation):
                    if detector_id in warnings:
                        warnings[detector_id].append(ch.ecode)
                    else:
                        warnings[detector_id] = [ch.ecode]

            rule_warnings: Dict[str, List] = {}

            for check in RuleCheck.__subclasses__():
                logging.debug("Processing alert check %s" % check.ecode)

                result = check().process(
                    detector, events, incidents, computation
                )
                if len(result):
                    if detector_id not in rule_warnings:
                        rule_warnings[detector_id] = {}

                    for rule_id, ecode in result.items():
                        if rule_id in rule_warnings[detector_id].keys():
                            rule_warnings[detector_id][rule_id].append(ecode)
                        else:
                            rule_warnings[detector_id][rule_id] = [ecode]

            logging.error("Detector checks: %s" % warnings)
            logging.error("Alert rule checks: %s" % rule_warnings)

            if format == "json":
                print(
                    json.dumps(
                        {"warnings": warnings, "rule_warnings": rule_warnings},
                        sort_keys=True,
                        indent=4,
                    )
                )

            computation.close()


if __name__ == "__main__":
    main()
