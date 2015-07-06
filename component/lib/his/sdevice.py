import snetwork.httpclient as httpclient
import snetwork.httputils as httputils
import os
import json
import argparse
import time
from log.log import *
import urllib
from log.log import *

class sdevice(object):
    def __init__(self,guid):
        self.device_core = httputils.find_lan_device(guid)
        self.guid = guid
        if self.valid():
            self.address = self.device_core.address
            self.port = self.device_core.port
            print_info("Get device %s at %s:%d" % (guid,self.address,self.port))
        
    def do(self,verb='',action={},timeout=5):
        if self.valid():
            action_string = "http://%s:%d/%s" % (self.address,self.port,verb)
            actions = []
            for k in action.keys():
                actions.append("%s=%s" % (k,urllib.quote(action[k])))
            if len(actions) > 0:
                action_string += '?'
                action_string += "&".join(actions)
            resp = httpclient.get(action_string,timeout)
            if resp != '':
                repo = json.loads(resp)
                return repo
            else:
                print_error("Device %s Action failed : %s" % (self.guid,action_string))
                return None
                
        print_error("Device %s is not valid" % self.guid)
        return None
    
    def valid(self):
        if self.device_core is None:
            return False
        return True

def get_device(guid):
    d = sdevice(guid)
    if not d.valid():
        print_error("Device %s is not valid" % guid)
    return d