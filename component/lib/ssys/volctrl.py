import platform

if platform.system() == 'Windows':
    from volctrl_win32 import *
elif platform.system() == 'Darwin':
    from volctrl_osx import *
else:
    print 'Error Not Implemented'