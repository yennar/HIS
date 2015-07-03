from urlparse import urlparse, parse_qs
import socket
import re
from ping import *
from base.his import *
import httpclient
import json

def get_filepath_from_httppath(httppath):
    p = urlparse(httppath)
    return p.path

def get_query_from_httppath(httppath):
    p = urlparse(httppath)
    h = parse_qs(p.query)
    r = {}
    for k in h.keys():
        r[k] = h[k][0]
    return r

class lan_addr_port(object):
    address = '0.0.0.0'
    port = 0

def find_lan_device_by_guid(guid):
    my_ip = socket.gethostbyname(socket.gethostname())
    my_ip_abc = re.sub(r'\d+$','',my_ip)
    for d in xrange(1,256):
        dest_addr = "%s%d" % (my_ip_abc,d)
        list_url = "http://%s:%d/list" % (dest_addr,HIS_HOSTHUB_ROOT_PORT)
        resp = httpclient.get(list_url,timeout=1)
        if resp != '':
            resp = json.loads(resp)
            data = resp.get('data')
            if data is not None and type(data) == type({}):
                if guid in data.keys():
                    rtn = lan_addr_port()
                    rtn.address = dest_addr
                    rtn.port = data[guid]['port']
                    return rtn

if __name__ == '__main__':
    print find_lan_device_by_guid('b318fd7f-5182-4662-8691-a68fbfbaf182')