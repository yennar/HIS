#from PyQt import *
import os
import BaseHTTPServer
import argparse
import sys
import json
from log.log import *
import httpclient
from base.his import *
import time

class handle(BaseHTTPServer.BaseHTTPRequestHandler):
    tag = ''
    storage_path = ''
    log_path = ''
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
    parser.add_argument('-s', '--storage',default='',type=str)
    parser.add_argument('-l', '--log',default='',type=str)
    result = parser.parse_args()
    guid = result.guid
    
    if guid == '':
        print_error("-guid must be specified")
        exit(1)
        
    run_port = None
    if is_hosthub == False:
        #connect to hub
        resp = ''
        while resp == '':
            resp = httpclient.get('http://127.0.0.1:%d/add?guid=%s' % (HIS_HOSTHUB_ROOT_PORT,guid))
            time.sleep(5)
            
        hub_result = json.loads(resp)
        run_port = hub_result.get('data',0)
        if run_port == 0:
            print_error("Failed to register to hub")
            exit(1)
        else:
            result.storage = hub_result.get('storage','')
            result.log = hub_result.get('log_file','')
            os.environ['HIS_LOG_FILE'] = result.log
            os.environ['HIS_STORAGE'] = result.storage
            print_info("Connected to hub")
    else:
        run_port = HIS_HOSTHUB_ROOT_PORT
        
    if result.storage == '':
        print_error("Failed to locate storage path, run with -s or check the hub")
        exit(1)
        
    if result.log == '':
        result.log = result.storage + '/var/log/'
            
    if is_hosthub:
        try:
            os.makedirs(result.log)
            os.makedirs(result.storage)
        except:
            pass        
        os.environ['HIS_LOG_FILE'] = result.log + '/' + guid + '.log'
        handler_class.storage_path = result.storage
        handler_class.log_path = result.log        
    
    os.environ['HIS_APP_GUID'] = guid
    print_info("Start Server at port %d with tag '%s'" % (run_port,result.tag))
    server_address = ('', run_port)
    handler_class.tag = result.tag

    httpd = BaseHTTPServer.HTTPServer(server_address, handler_class)
    httpd.serve_forever()
    