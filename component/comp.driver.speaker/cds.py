import pyttsx
import os
import sio.serial as serial
import snetwork.httpserver as httpserver
import snetwork.httputils as httputils
from base.qt import *
from log.log import *
import time

class cds_handle(httpserver.handle):
    engine = None 
    def on_get(self, httppath):
        path = httputils.get_filepath_from_httppath(httppath)
        query = httputils.get_query_from_httppath(httppath)
        rtn = {
            'path' : path,
            'time' : int(time.time())
        }   
        if path == '/say' and query.get('content') is not None:
            content = query.get('content')
            print_info(content)
            if cds_handle.engine is None:
                cds_handle.engine = pyttsx.init()
                rate = cds_handle.engine.getProperty('rate')
                cds_handle.engine.setProperty('rate', rate-60)                
            cds_handle.engine.say(content)
            cds_handle.engine.runAndWait()
            
        return self.wrap_data(rtn)

httpserver.run(cds_handle)
