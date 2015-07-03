#from PyQt import *
import os
import BaseHTTPServer
import argparse
import sys
import json
from log.log import *
import httpclient
from base.his import *

class handle(BaseHTTPServer.BaseHTTPRequestHandler):
    tag = ''
    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
    
    def do_GET(self):
        rtn = self.on_get(self.path)
        data = rtn['data']
        
        if rtn['type'] == 'application/json' or rtn['type'] == 'json':
            rtn['type'] == 'application/json'
            data = json.dumps(data, sort_keys=True,indent=4, separators=(',', ': '))
            
        self.send_response(200)
        self.send_header('Content-Type',rtn['type'])
        self.end_headers()    
        self.wfile.write(data)    
    
    def on_get(self,path):
        return self.wrap_data(data_type='json',data_body={'path':path})
    
    def wrap_data(self,data_body = {},data_type = 'application/json'):
        return {
            'type' : data_type,
            'data' : data_body
        }
    

def run(handler_class=handle,run_port=None,is_hosthub=False):
    #app = QCoreApplication(sys.argv)
    parser = argparse.ArgumentParser(prog='HTTP_SERVER')
    parser.add_argument('-g', '--guid',default='',type=str)
    parser.add_argument('-t', '--tag',default=handler_class.tag,type=str)
    result = parser.parse_args()
    guid = result.guid
    
    if guid == '':
        print_error("-guid must be specified")
        exit(1)
        
    run_port = None
    if is_hosthub == False:
        #connect to hub
        hub_result = json.loads(httpclient.get('http://127.0.0.1:%d/add?guid=%s' % (HIS_HOSTHUB_ROOT_PORT,guid)))
        run_port = hub_result.get('data',0)
        if run_port == 0:
            print_error("Failed to register to hub")
            exit(1)
        else:
            pass
    else:
        run_port = HIS_HOSTHUB_ROOT_PORT
    
    print_info("Start Server at port %d with tag '%s'" % (run_port,result.tag))
    server_address = ('', run_port)
    handler_class.tag = result.tag
    httpd = BaseHTTPServer.HTTPServer(server_address, handler_class)
    httpd.serve_forever()
    