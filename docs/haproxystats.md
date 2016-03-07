# HAProxyServer

HAProxyServer represents a single HAProxy instance. Stores corresponding frontend, backend, and listener services.

**Params**:

* base_url (str): hostname:port or ip:port of this HAProxy instance
* user (str):  User to authenticate with via basic auth(optional)
* password(str):  Password to authenticate with via basic auth(optional)
* verify_ssl(bool): Fail on SSL validation error. Default True

**Attrs**:

* failed (bool): Whether the last update attempt failed
* last_update (obj): datetime.datetime object of last update time in UTC
* frontends (list): List of haproxy.HAProxyService objects identified as frontends
* backends (list): List of haproxy.HAProxyService objects identified as backends
* listeners (list):  List of haproxy.HAProxyService objects identified as backend listeners

****

## update

Fetches latest stats for this HAProxy server

**Returns**: None

## to_json

**Returns** (str): JSON-encoded representation of all frontend, backend, and listener stats

# HAProxyService

HAProxyService represents a single frontend, backend, or listener

**Attrs**:

All service stats are stored as attributes and can vary base on HAProxy verision.

* proxy_name(str): The HAProxy server this service belongs to
* name(str): The service name, unique to the HAProxy server 
