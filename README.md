# haproxy-stats
[![Documentation Status](https://readthedocs.org/projects/haproxy-stats/badge/?version=latest)](http://haproxy-stats.readthedocs.org/en/latest/haproxystats/)

Haproxy-stats is a small Python library for fetching and parsing realtime stats from HAProxy

# Installing
```
pip install haproxy-stats
```

# Usage
```python
from haproxystats import HAProxyServer

haproxy = HAProxyServer('127.0.0.1:3212')

for b in haproxy.backends:
    print('%s: %s' % (b.name, b.status))
```
```
backend1: UP
backend2: UP
backend3: UP
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
