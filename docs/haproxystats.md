# HaproxyStats

HaproxyStats class for fetching and parsing from an arbitrary number of HAProxy stat sockets. Stats will be gathered initially on instantiation and can be updated with the update() method described below.

**Params**:

* base_urls (list): List of HAProxy urls defined as hostname:port or ip:port
* user (str):  User to authenticate with via basic auth(optional)
* user_pass (str):  Password to authenticate with via basic auth(optional)

**Attrs**:

* servers (list): List of haproxystats.HAProxyServer objects

****

## update

Polls all servers for updated stats

**Returns** (bool): True if all servers were successfully polled

## to_json

**Returns** (str): JSON-encoded stats for all servers


# HAProxyServer

HAProxyServer represents a single HAProxy instance. Stores corresponding frontend, backend, and listener services.

**Params**:

* base_url (str): hostname:port or ip:port of this HAProxy instance
* user (str):  User to authenticate with via basic auth(optional)
* user_pass (str):  Password to authenticate with via basic auth(optional)

**Attrs**:

* failed (bool): Success of latest attempt to fetch stats
* last_update (obj): datetime.datetime object of last update time in UTC
* frontends (list): List of haproxy.HAProxyService objects identified as frontends
* backends (list): List of haproxy.HAProxyService objects identified as backends
* listeners (list):  List of haproxy.HAProxyService objects identified as backend listeners
* stats (dict): Structured dictionary of all frontends,backends,and listener dicts

****

## fetch_stats

Fetches latest stats for this HAProxy server

**Returns**: None

# HAProxyService

HAProxyService represents a single frontend, backend, or listener

**Attrs**:

All service stats are stored as attributes and can vary base on HAProxy verision.

* proxy_name(str): The HAProxy server this service belongs to
* name(str): The service name, unique to the HAProxy server 
