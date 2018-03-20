import json
import logging
from datetime import datetime
from requests import Session

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.WARN)

class HAProxyServer(object):
    """
    Represents a single HAProxy instance to be polled
    params:
     - base_url(list) - HAProxy url defined as <host>:<stats-port>
     - user(str) -  User to authenticate with via basic auth(optional)
     - password(str) -  Password to authenticate with via basic auth(optional)
     - verify_ssl(bool) - Fail on SSL validation error. Default True.
    """
    def __init__(self, base_url, user=None, password=None,
                 verify_ssl=True, timeout=5, https=False):
        self.failed = False
        self.verify = verify_ssl
        self.timeout = timeout
        self._session = Session()
        if user and password:
            self._session.auth = (user, password)

        self.name = base_url.split(':')[0]
        if https:
            base_url = 'https://'+base_url
        else:
            base_url = 'http://'+base_url
        self.url = base_url + '/;csv;norefresh'

        self.update()

    def update(self):
        """ Fetch and parse stats """
        self.frontends = []
        self.backends = []
        self.listeners = []

        csv = [ l for l in self._fetch().strip(' #').split('\n') if l ]
        if self.failed:
            return

        #read fields header to create keys
        self.fields = [ f for f in csv.pop(0).split(',') if f ]
    
        #add frontends and backends first
        for line in csv:
            service = HAProxyService(self.fields, line.split(','), self.name)

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
                    backend.listeners.append(listener)

        self.last_update = datetime.utcnow()

    def to_json(self):
        services = { 'frontends': self.frontends, 'backends': self.backends }
        return json.dumps({ self.name : services }, cls=Encoder)
    
    def _fetch(self):
        try:
            r = self._session.request('GET', self.url,
                                      timeout=self.timeout,
                                      verify=self.verify)
        except Exception as ex:
            self._fail(ex)
            return ""

        if not r.ok:
            self._fail(r.text)
            return ""

        return r.text

    def _fail(self, reason):
        self.failed = True
        log.error('Error fetching stats from %s:\n%s' % (self.url, reason))


class HAProxyService(object):
    """
    Generic service object representing a frontend, backend, or listener
    params:
     - fields(list): Fieldnames as read from haproxy stats export header
     - values(list): Values for corresponding fields
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

class Encoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, '__dict__'):
            return obj.__dict__
        else:
            return json.JSONEncoder.default(self, obj)
