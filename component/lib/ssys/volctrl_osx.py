from osax import *


class VolCtrl(object):
    def __init__(self):
        self.sa = OSAX()

    def mastervol_up(self):
        pass

    def mastervol_down(self):
        pass

    @property
    def mastervol(self):
        s = self.sa.get_volume_settings()
        return s[k.output_volume]

    @mastervol.setter
    def mastervol(self, vol):
        self.sa.set_volume(vol)
        
        
if __name__ == '__main__':
    vc = VolCtrl()
    print vc.mastervol
    vc.mastervol = 100
    print vc.mastervol