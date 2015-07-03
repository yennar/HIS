import os
import sio.serial as serial
import snetwork.httpserver as httpserver
from base.qt import *
from log.log import *
import time

class cmt_handle(httpserver.handle):
    serial_port = None
    tag = 'USB Serial Port'
    def on_get(self, path):
        rtn = {
            'path' : path,
            'time' : int(time.time())
        }
        if path == '/type':
            rtn['type'] = 'char'
        elif path == '/data':
            if cmt_handle.serial_port is None:
                cmt_handle.serial_port = serial.HisSerial(cmt_handle.tag)
                if not cmt_handle.serial_port.open(QIODevice.ReadOnly):
                    rtn['status'] = 'Serial Open Failed'
                    cmt_handle.serial_port = None
                else:
                    cmt_handle.serial_port.setBaudRate(9600)
            if cmt_handle.serial_port is not None:
                if cmt_handle.serial_port.waitForReadyRead(-1):
                    ch = cmt_handle.serial_port.readAll()
                    rtn['data'] = ord(ch[0])
                else:
                    print_error("Error Code %d" % cmt_handle.serial_port.error())
        return self.wrap_data(rtn)

httpserver.run(cmt_handle)

