import os
from base.qt import *
from log.log import *
from smath.matrix import *

class HisSerial(QSerialPort):
    def __init__(self,query_name):
        QSerialPort.__init__(self)
        
        name_matrix = {}
        name_id = 0
        for sys_port in QSerialPortInfo.availablePorts():
            print_info("Port %s,%s" % (sys_port.portName(),sys_port.systemLocation()))
            name_matrix[name_id] = {
                0:sys_port.portName(),
                1:sys_port.manufacturer(),
                2:sys_port.description(),
                3:sys_port.systemLocation()
            }
            name_id += 1
        
        find_flag = 0
        name_matrix = matrix_rotate(name_matrix)
        port_name = None
        for name_id in name_matrix.keys():
            if find_flag:
                break
            for item_id in name_matrix[name_id].keys():
                v = name_matrix[name_id][item_id]
                if v == query_name:
                    port_name = name_matrix[0][item_id]
                    find_flag = 1
                    break
        if find_flag:
            self.setPortName(port_name)
            print_info("Select Port %s" % port_name)
        else:
            print_error("Cannot search port keyword %s" % query_name)
        
if __name__ == '__main__':
    p = HisSerial('USB Serial Port')