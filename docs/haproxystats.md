# HaproxyStats

HaproxyStats class for fetching and parsing from an arbitrary number of Haproxy stat sockets. Stats will be gathered initially on instantiation and can be updated with the update() method described below.

**Params**:

* base_urls (list): List of haproxy instances defined as hostname:port or ip:port
* user (str):  User to authenticate with via basic auth(optional)
* user_pass (str):  Password to authenticate with via basic auth(optional)

**Attrs**:

* servers (list): Dictionary of all servers, frontends, backends, and listeners
* last_update (obj): datetime.datetime object of last update time in UTC

****

## update

Polls all servers for updated stats

**Returns** (bool): True if all servers were successfully polled

## to_json

**Returns** (str): JSON-encoded stats for all servers

