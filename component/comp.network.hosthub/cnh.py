import os
import snetwork.httpserver as httpserver
import snetwork.httputils as httputils
from base.his import *
from log.log import *
import time


cnh_devices = {}
cnh_port_pool = {}
cnh_port_start = HIS_HOSTHUB_ROOT_PORT

class cnh_handle(httpserver.handle):
    def on_get(self, httppath):
        path = httputils.get_filepath_from_httppath(httppath)
        query = httputils.get_query_from_httppath(httppath)
        rtn = {
            'path' : path,
            'time' : int(time.time())
        }        
        # Case: from all
        if path == '/list':
            rtn['data'] = cnh_devices
        # Case: from internal devices
        elif path =='/add' and self.client_address[0] == '127.0.0.1':
            global cnh_port_start
            device_guid = query.get('guid')
            device_port = 0
            device_info = 'Error'
            if device_guid is None:
                device_info = 'No GUID specified'
            else:
                device_port = cnh_port_pool.get(device_guid)
                if device_port is None:
                    cnh_port_start += 1
                    print_info("Create port %d for guid %s" % (cnh_port_start,device_guid))
                    device_port = cnh_port_start
                    cnh_port_pool[device_guid] = device_port
                query['port'] = device_port
                cnh_devices[device_guid] = query
                device_info = 'OK'
            rtn['data'] = device_port
            rtn['info'] = device_info

            device_storage_path = self.storage_path + '/storage/' + device_guid
            try:
                os.makedirs(device_storage_path)
            except:
                pass
            
            if os.path.isdir(device_storage_path):
                rtn['storage'] = device_storage_path
            
            device_log_path = self.log_path + '/'

            try:
                os.makedirs(device_log_path)
            except:
                pass
            
            if os.path.isdir(device_log_path):
                rtn['log_file'] = device_log_path + '/' + device_guid + '.log'            
            
        return self.wrap_data(rtn)

httpserver.run(cnh_handle,HIS_HOSTHUB_ROOT_PORT,True)
