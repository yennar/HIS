QT_VER = None
import os

try:
    from PyQt5.QtCore import * 
    from PyQt5.QtGui import *
    from PyQt5.QtWidgets import *
    from PyQt5.QtSql import *
    from PyQt5.QtXml import *
    from PyQt5.QtSerialPort import *
    from PyQt5.QtMultimedia import *
    from PyQt5.QtMultimediaWidgets import *
    QT_VER = 5
except:
    if os.getenv("USE_QT4",None):
        from PyQt4.QtCore import * 
        from PyQt4.QtGui import *
        from PyQt4.QtSql import *
        from PyQt4.QtXml import *
        QT_VER = 4
    
    if os.getenv("USE_QT5",None):
        from PyQt5.QtCore import * 
        from PyQt5.QtGui import *
        from PyQt5.QtWidgets import *
        from PyQt5.QtSql import *
        from PyQt5.QtXml import *
        from PyQt5.QtSerialPort import *
        from PyQt5.QtMultimedia import *
        from PyQt5.QtMultimediaWidgets import *        
        QT_VER = 5
        
if QT_VER is None:
    print "[ERROR] Select QT_VER before import qt"
    exit(1)

print "[INFO] Using Qt%d" % QT_VER