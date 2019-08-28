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


# Output

The output contains per-rule and whole-detector checks. The findings are emitted as string "names" that can be mapped to feedback i18n style.

Example of `json` output formatted output:
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
