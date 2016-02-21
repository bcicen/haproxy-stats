# haproxy-stats
[![Documentation Status](https://readthedocs.org/projects/haproxy-stats/badge/?version=latest)](http://haproxy-stats.readthedocs.org/en/latest/?badge=latest)

Haproxy-stats is a small Python library for fetching and parsing realtime stats from HAProxy

# Installing
```
pip install haproxy-stats
```

# Usage
```python
from haproxystats import HAProxyServer

haproxy = HAProxyServer('127.0.0.1:3212', user='<username>', password='<password>')

for l in haproxy.listeners:
    print('%s: %s' % (l.name, l.status))
```
```
backend_listener1: UP
backend_listener2: UP
backend_listener3: UP
backend_listener4: UP
```

```python
haproxy.to_json()
```

```json
{
  "127.0.0.1": {
    "backends": [
      {
        "status": "UP",
        "lastchg": 497805,
        "weight": 0,
         "..."
        "listeners": []
      }
    ],
    "frontends": []
  }
}
```

full docs available in the docs/ folder
