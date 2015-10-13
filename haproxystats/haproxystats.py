import json
import logging
from datetime import datetime
from requests import Request, Session

log = logging.getLogger(__name__)

class HAProxyStatsException(Exception):
    """ Generic HAProxyStats exception """

class HAProxyService(object):
    """
    Generic service object representing a proxy component
    params:
     - fields(list): Fieldnames as read from haproxy stats export header
     - values(list): Stats for corresponding fields given above for this 
                     frontend, backend, or listener
     - proxy_name(str): Common name of the proxy this service belongs to
    """
    def __init__(self, fields, values, proxy_name):
        values = [ self._decode(v) for v in values ]

        #zip field names and values
        self.__dict__ = dict(zip(fields, values))

        if self.svname == 'FRONTEND' or self.svname == 'BACKEND':
            self.name = self.pxname
        else:
            self.name =  self.svname

        self.proxy_name = proxy_name

    @staticmethod
    def _decode(value):
        """
        decode byte strings and convert to int where needed
        """
        if value.isdigit():
            return int(value)
        if isinstance(value, bytes):
            return value.decode('utf-8')
        else:
            return value

class HAProxyServer(object):
    """
    HAProxyServer object is created for each haproxy server polled. Stores
    corresponding frontend, backend, and listener services.
    params:
     - user(str) -  User to authenticate with via basic auth(optional)
     - password(str) -  Password to authenticate with via basic auth(optional)
     - verify_ssl(bool) - Fail on SSL validation error. Default True.
    """
    def __init__(self, base_url, user=None, password=None, verify_ssl=True):
        self.failed = False
        self.verify = verify_ssl
        self.auth = (user,password)

        self.name = base_url.split(':')[0]
        self.url = 'http://' +  base_url + '/;csv;norefresh'

    def fetch_stats(self):
        """
        Fetch and parse stats from this Haproxy instance
        """
        self.frontends = []
        self.backends = []
        self.listeners = []

        csv = [ l for l in self._poll().strip(' #').split('\n') if l ]
        if self.failed:
            return

        #read fields header to create keys
        fields = [ f for f in csv.pop(0).split(',') if f ]
    
        #add frontends and backends first
        for line in csv:
            service = HAProxyService(fields, line.split(','), self.name)

            if service.svname == 'FRONTEND':
                self.frontends.append(service)
            elif service.svname == 'BACKEND':
                service.listeners = []
                self.backends.append(service)
            else:
                self.listeners.append(service)
    
        #now add listener  names to corresponding backends
        for listener in self.listeners:
            for backend in self.backends:
                if backend.iid == listener.iid:
                    backend.listeners.append(listener.__dict__)

        self.stats = { 'frontends': [ s.__dict__ for s in self.frontends ],
                       'backends': [ s.__dict__ for s in self.backends ] }

        self.last_update = datetime.utcnow()
    
    def _poll(self):
        s = Session()

        if None in self.auth:
            req = Request('GET', self.url)
        else:
            req = Request('GET', self.url, auth=self.auth)

        try:
            r = s.send(req.prepare(), timeout=10, verify=self.verify)
        except Exception as ex:
            self._fail(ex)

        if not r.ok:
            self._fail(r.text)

        return r.text

    def _fail(self, reason):
        self.failed = True
        raise HAProxyStatsException('Error fetching stats from %s:\n%s' % \
                                    (self.url, reason))

class HaproxyStats(object):
    """
    Manage multiple HAProxyServer instances.
    params:
     - base_urls(list) - List of haproxy instances defined as
       hostname:port or ip:port
     - user(str) -  User to authenticate with via basic auth(optional)
     - password(str) -  Password to authenticate with via basic auth(optional)
     - verify_ssl(bool) - Fail on SSL validation error. Default True.
    """
    def __init__(self, base_urls, user=None, password=None, verify_ssl=True):
        self.servers = []
        for s in base_urls:
            server = HAProxyServer(s, user=user, password=password,
                                   verify_ssl=verify_ssl)
            self.servers.append(server)

        self.update()

    def update(self):
        start = datetime.utcnow()

        for s in self.servers:
            s.fetch_stats()

        duration = (datetime.utcnow() - start).total_seconds()
        log.info('Polled stats from %s servers in %s seconds' % \
                (len(self.servers),duration))

        if self.get_failed():
            return False

        return True

    def to_json(self):
        return json.dumps({ s.name: s.stats for s in self.servers })

    def get_failed(self):
        return [ s for s in self.servers if s.failed ]
