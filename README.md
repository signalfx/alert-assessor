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

```
{
  'rule_problems':
    [
      [
        'E_RULE_MISSING_RUNBOOK_URL',
        'E_RULE_MISSING_TIP',
        'E_RULE_MISSING_PARAMETERIZED_SUBJECT',
        'E_RULE_MISSING_PARAMETERIZED_BODY'
      ]
    ],
    'problems': [
      'E_MISSING_TIMESERIES',
      'E_TOO_IMMATURE'
    ]
}
```
