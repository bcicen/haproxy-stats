import requests
import json
import logging

urls = [ 'server1:3212', 'server2:3212' ]

logging.basicConfig(level=logging.WARN)
log = logging.getLogger(__name__)


def to_utf(u):
    return u.encode('utf8')

def read_stat(stat):
    """
    Read stat str, convert unicode to utf and string to int where needed
    and return as list
    """
    ret = []
    for s in stat.split(','):
        if s.isdigit():
            s = int(s)
        if isinstance(s,unicode):
            s = to_utf(s)
        ret.append(s)

    return ret

def fetch_and_parse(base_url):
    """
    Fetch and parse stats from a single haproxy instance
    """

    local_stats = { 'frontends': {}, 'backends':  {} }
    haproxy_url = 'http://' +  base_url + '/;csv;norefresh'

    r = requests.get(haproxy_url, auth=(user, user_pass))

    csv = r.text.strip(' #').split('\n')
    fields = [ to_utf(f) for f in csv.pop(0).split(',') if f ]

    stats = [ dict(zip(fields, read_stat(l))) for l in csv if l ]

    #populate frontends and backends first
    listeners = []
    for stat in stats:
        name = stat['pxname']

        if stat['svname'] == 'FRONTEND':
            local_stats['frontends'][name] = stat

        elif stat['svname'] == 'BACKEND':
            stat['listeners'] = {}
            local_stats['backends'][name] = stat

        else:
            listeners.append(stat)

    #now add servers/listeners to corresponding backends
    for stat in listeners:
        name = stat['svname'] #use unique svname here
        iid = stat['iid']
        for bkname,bkend in local_stats['backends'].iteritems():
            if bkend['iid'] == iid:
                bkend['listeners'][name] = stat

    return local_stats

def main():
    all_stats = { url.split(':')[0] : fetch_and_parse(url) for url in urls }
    print(json.dumps(all_stats))

if __name__ == '__main__':
    main()
