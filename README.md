# haproxy-stats
Haproxy-stats is a small Python library for fetching and parsing servers stats from HAProxy

# Installing
```
git clone https://github.com/bcicen/haproxy-stats.git
cd haproxy-stats/
pip install -r requirements.txt
python setup.py install
```

# Usage
```python
from haproxystats import HaproxyStats

base_urls = [ 'server1:3212', 'server2:3212' ]
hs = HaproxyStats(base_urls,user='<username>',user_pass='<password>')

for server in hs.servers:
    for l in server.listeners:
        print l.status
```
```
UP
UP
UP
```

```python
print(hs.to_json())
```

```json
{
  "haproxy_server1": {
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
