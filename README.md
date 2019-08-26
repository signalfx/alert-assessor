# SignalFx Alert Assessor

> Annoying alerts got you agitated? Allocate some attention to an apt agent that assesses your alerts and advances alms to alleviate your angst, assuage your ailments, and ameliorate your awareness.

The Alert Assessor looks at a detector and tells you how it can be *improved*.

# Usage

```
SFX_AUTH_KEY=<AUTH_KEY> python alert-assessor.py <ALERTID>
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
