# haproxy-stats
Haproxy-stats is a small Python library for east fetching and parsing of one or several Haproxy server stat sockets

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

servers = [ 'server1:3212', 'server2:3212' ]

hs = HaproxyStats(servers,user='<username>',user_pass='<password>')

hs.to_json()
...
```

# Stat Structure

All frontend,backend, and listener stats read like so:
```
{
 "name":
   "field1":"value1",
   "field2":"value2"
}
```

Each stat is structured cummulatively according to the server or backend(in the case of listeners) they are a member of:
```
{
  "haproxy_server1": {
    "backends": {
      "backend1":
				...
        "listeners": {
          "listener1": {...}
        }
		},
    "frontends": {...}
  }
}
```
