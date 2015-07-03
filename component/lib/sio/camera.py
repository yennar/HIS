import os
from base.qt import *
from log.log import *
from smath.matrix import *

class HisVideoSurface(QAbstractVideoSurface):
    def __init__(self,handle):
        QAbstractVideoSurface.__init__(self)
        self.handle = handle
        self.image = None
        
    def supportedPixelFormats(self,t):
        return [QVideoFrame.Format_RGB32,QVideoFrame.Format_RGB24]

    def present(self,frame = QVideoFrame()):
        if frame.isValid():
            cloneFrame = QVideoFrame(frame)
            cloneFrame.map(QAbstractVideoBuffer.ReadOnly)
            self.image =  QImage (cloneFrame.bits(),
                         cloneFrame.width(),
                         cloneFrame.height(),
                         QVideoFrame.imageFormatFromPixelFormat(cloneFrame.pixelFormat()))
            cloneFrame.unmap()
            return True
        return False

class HisCamera(QObject):
    def __init__(self,query_name = None,handle = QObject()):
        QObject.__init__(self)
        self.camera = None
        self.handle = handle
        name_matrix = {}
        name_id = 0
        for sys_camera in QCameraInfo.availableCameras():
            print_info("Camera %s,%s" % (sys_camera.description(),sys_camera.deviceName()))
            name_matrix[name_id] = {
                0:sys_camera.description(),
                1:sys_camera.deviceName()
            }
            name_id += 1

        if name_id == 1 and query_name is None:
            device_name = name_matrix[0][1]
            find_flag = 1
        else:
            if query_name is None:
                query_name = ''
            find_flag = 0
            name_matrix = matrix_rotate(name_matrix)
            device_name = None
            for name_id in name_matrix.keys():
                if find_flag:
                    break
                for item_id in name_matrix[name_id].keys():
                    v = name_matrix[name_id][item_id]
                    if v == query_name:
                        device_name = name_matrix[0][item_id]
                        find_flag = 1
                        break
                
        if find_flag:
            self.camera = QCamera(device_name)
            self.camera_capture = QCameraImageCapture(self.camera)
            self.viewfinder = HisVideoSurface(self.handle)
            
            self.camera.setViewfinder(self.viewfinder)            
            self.camera.setCaptureMode(QCamera.CaptureStillImage)
            self.camera.start()
            
            print_info("Select Device %s" % device_name)
        else:
            print_error("Cannot search camera keyword %s" % query_name)

    def read(self):
        if self.camera is None:
            return None
        return self.viewfinder.image
    
if __name__ == '__main__':
    app = QApplication([])
    c = HisCamera()
    image = c.read()
    if image is not None:
        print image.size()
    app.exec_()
    
