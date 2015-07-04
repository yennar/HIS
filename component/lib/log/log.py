import sys
import os
import time

__h = None

class log_handle(object):
    def __init__(self,filename):
        self.sys_stdout = sys.stdout
        self.filehandle = open(filename,'a')
        sys.stdout = self
        
    def write(self,w):
        self.sys_stdout.write(w)
        self.filehandle.write(w)
        self.filehandle.flush()
        self.sys_stdout.flush()
        
def __print_string(c,s):
    global __h
    if os.getenv("HIS_LOG_FILE",None) and __h is None:
        __h = log_handle(os.getenv("HIS_LOG_FILE"))
    print c,time.strftime("%Y-%m-%d,%H:%M:%S"),s
    
def print_info(log_str):
    __print_string('[INFO]',log_str)
    
def print_error(log_str):
    __print_string('[ERROR]',log_str)