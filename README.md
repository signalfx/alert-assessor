>ℹ️&nbsp;&nbsp;SignalFx was acquired by Splunk in October 2019. See [Splunk SignalFx](https://www.splunk.com/en_us/investor-relations/acquisitions/signalfx.html) for more information.

# SignalFx Alert Assessor

> Annoying alerts got you agitated? Allocate some attention to an apt agent that assesses your alerts and advances alms to alleviate your angst, assuage your ailments, and ameliorate your awareness.

The Alert Assessor looks at a detector and tells you how it can be *improved*.

# Usage

```
Usage: alert-assessor.py [OPTIONS] DETECTOR_ID

Options:
  --sfx_auth_key TEXT     SFX token (or SFX_AUTH_KEY env variable)
  --api_endpoint TEXT     API endpoint
  --stream_endpoint TEXT  Stream endpoint
  --help                  Show this message and exit.
```

or you can provide the token in `SFX_AUTH_KEY` env var
```
SFX_AUTH_KEY=<AUTH_KEY> ./alert-assessor.py DETECTOR_ID
```

# Features

The assessor can spot detectors with the following conditions:

* "immature" that might not have enough information to be accurately assessed.
* have not generated any alerts in the last 30 days, do they work?
* have never fired!
* too noisy, firing at least once a day
* no rules, what is this even doing?
* missing time series, metric gone?
* too many time series, detector is dropping stuff
* unlike aggregation terms
* alerts that have been active (and probably ignored) for a long time
* no runbook
* no tip
* doesn't notify anyone
* not using a parameterized subject or body
* not using any variables in parameterized body or subject

# Output

The output contains per-rule and whole-detector checks. The findings are emitted as string "names" that can be mapped to feedback i18n style in addition to helper text.

Here's an example of the default output:

```
INFO:root:Registered 16 rule(s)
ERROR:root:Alert rule checks
INFO:root:	EC5zlmcAcAA: Rule: 0 E_RULE_MISSING_NOTIFICATIONS
	No notifications
	An alert with no notifications cannot alert anyone. Consider removing or adding notifications.

INFO:root:	EC5zlmcAcAA: Rule: 0 E_RULE_NOVARS_PARAMETERIZED_BODY
	No parameterized body vars
	Using a parameterized body with no vars misses out in improved context. Consider adding tags from the alert result.
```

And an example of `json` output formatted output:
```
{
    "rule_warnings": {
        "EC5zlmcAcAA": {
            "0": [
                {
                    "description": "No notifications",
                    "error_code": "E_RULE_MISSING_NOTIFICATIONS",
                    "help": "An alert with no notifications cannot alert anyone. Consider removing or adding notifications."
                },
                {
                    "description": "No parameterized body vars",
                    "error_code": "E_RULE_NOVARS_PARAMETERIZED_BODY",
                    "help": "Using a parameterized body with no vars misses out in improved context. Consider adding tags from the alert result."
                }
            ]
        }
    },
    "warnings": {
        "EC5zlmcAcAA": [
            {
                "description": "Not old enough to draw much from",
                "error_code": "E_TOO_IMMATURE",
                "help": "Let this alert cook a bit longer and try again!"
            },
            {
                "description": "Some of the time series in this signalflow don't exist",
                "error_code": "E_MISSING_TIMESERIES",
                "help": "There are time series missing from this detector, which might mean the metrics have gone away and the alert needs adjusting or removal."
            }
        ]
    }
}
```

# TODO

This is definitely a work in progress. It can do so many things to help humans! Here's some stuff:

* Add more things!
* list detectors by pattern, and apply rules to all
* `.accessor.yaml`, where one can disable  or configure rules, or point at custom rules
  * Or perhaps in-alert pragma
* offer to fix things? are there even rules that this would make sense for?
* colorize output, because why not
* reduce boiler plate in RuleCheck
* add tests with JSON blobs from the API
