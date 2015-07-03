from comtypes import *


class IAudioEndpointVolume(IUnknown):
    _iid_   = GUID('{5CDF2C82-841E-4546-9722-0CF74078229A}')
    _methods_   = [
        COMMETHOD([], HRESULT, 'RegisterControlChangeNotify',
                  (['in'], c_voidp, 'pNotify')
        ),
        COMMETHOD([], HRESULT, 'UnregisterControlChangeNotify',
                  (['in'], c_voidp, 'pNotify')
        ),
        COMMETHOD([], HRESULT, 'GetChannelCount',
                  (['out'], POINTER(c_uint), 'pnChannelCount')
        ),
        COMMETHOD([], HRESULT, 'SetMasterVolumeLevel',
                  (['in'], c_float, 'fLevelDB'),
                  (['in'], c_voidp, 'pguidEventContext')
        ),
        COMMETHOD([], HRESULT, 'SetMasterVolumeLevelScalar',
                  (['in'], c_float, 'fLevel'),
                  (['in'], c_voidp, 'pguidEventContext')
        ),
        COMMETHOD([], HRESULT, 'GetMasterVolumeLevel',
                  (['out'], POINTER(c_float), 'pfLevelDB')
        ),
        COMMETHOD([], HRESULT, 'GetMasterVolumeLevelScalar',
                  (['out'], POINTER(c_float), 'pfLevel')
        ),
        COMMETHOD([], HRESULT, 'SetChannelVolumeLevel',
                  (['in'], c_uint, 'nChannel'),
                  (['in'], c_float, 'fLevelDB'),
                  (['in'], c_voidp, 'pguidEventContext')
        ),
        COMMETHOD([], HRESULT, 'SetChannelVolumeLevelScalar',
                  (['in'], c_uint, 'nChannel'),
                  (['in'], c_float, 'fLevel'),
                  (['in'], c_voidp, 'pguidEventContext')
        ),
        COMMETHOD([], HRESULT, 'GetChannelVolumeLevel',
                  (['in'], c_uint, 'nChannel'),
                  (['out'], POINTER(c_float), 'pfLevelDB')
        ),
        COMMETHOD([], HRESULT, 'GetChannelVolumeLevelScalar',
                  (['in'], c_uint, 'nChannel'),
                  (['out'], POINTER(c_float), 'pfLevel')
        ),
        COMMETHOD([], HRESULT, 'SetMute',
                  (['in'], c_int, 'bMute'),
                  (['in'], c_voidp, 'pguidEventContext')
        ),
        COMMETHOD([], HRESULT, 'GetMute',
                  (['out'], POINTER(c_bool), 'pbMute')
        ),
        COMMETHOD([], HRESULT, 'GetVolumeStepInfo',
                  (['out'], POINTER(c_uint), 'pnStep'),
                  (['out'], POINTER(c_uint), 'pnStepCount')
        ),
        COMMETHOD([], HRESULT, 'VolumeStepUp',
                  (['in'], c_voidp, 'pguidEventContext')
        ),
        COMMETHOD([], HRESULT, 'VolumeStepDown',
                  (['in'], c_voidp, 'pguidEventContext')
        ),
        COMMETHOD([], HRESULT, 'QueryHardwareSupport',
                  (['out'], POINTER(c_uint), 'pdwHardwareSupportMask')
        ),
        COMMETHOD([], HRESULT, 'GetVolumeRange',
                  (['out'], POINTER(c_float), 'pflVolumeMindB'),
                  (['out'], POINTER(c_float), 'pflVolumeMaxdB'),
                  (['out'], POINTER(c_float), 'pflVolumeIncrementdB')
        )
    ]
                


class IMMDevice(IUnknown):
    _iid_   = GUID('{D666063F-1587-4E43-81F1-B948E807363F}')
    _methods_   = [
        COMMETHOD([], HRESULT, 'Activate',
                  (['in'], POINTER(GUID), 'iid'),
                  (['in'], c_uint, 'dwClsCtx'),
                  (['in'], c_voidp, 'pActivationParams'),
                  (['out'], POINTER(POINTER(IAudioEndpointVolume)), 'ppInterface')
        ),
        COMMETHOD([], HRESULT, 'OpenPropertyStore',
                  (['in'], c_int32, 'stgmAccess'),
                  (['out'], c_voidp, 'ppProperties')
        ),
        COMMETHOD([], HRESULT, 'GetId',
                  (['out'], c_voidp, 'ppstrId')
        ),
        COMMETHOD([], HRESULT, 'GetState',
                  (['out'], POINTER(c_uint), 'pdwState')
        )
    ]

class IMMDeviceEnumerator(IUnknown):
    _iid_   = GUID('{A95664D2-9614-4F35-A746-DE8DB63617E6}')
    _methods_   = [
        COMMETHOD([], HRESULT, 'EnumAudioEndpoints',
                  (['in'], c_int, 'dataFlow'),
                  (['in'], c_int, 'dwStateMask'),
                  (['out'], POINTER(c_voidp), 'ppDevices')
        ),
        COMMETHOD([], HRESULT, 'GetDefaultAudioEndpoint',
                  (['in'], c_int, 'dataFlow'),
                  (['in'], c_int, 'role'),
                  (['out'], POINTER(POINTER(IMMDevice)))
        ),
        COMMETHOD([], HRESULT, 'GetDevice',
                  (['in'], c_voidp, 'pwstrId'),
                  (['out'], POINTER(POINTER(IMMDevice)))
        ),
        COMMETHOD([], HRESULT, 'RegisterEndpointNotificationCallback',
                  (['in'], c_voidp)
        ),
        COMMETHOD([], HRESULT, 'UnregisterEndpointNotificationCallback',
                  (['in'], c_voidp)
        )
    ]




class VolCtrl(object):
    def __init__(self):
        clsid   = GUID('{BCDE0395-E52F-467C-8E3D-C4579291692E}')
        pMde = CoCreateInstance(clsid, interface=IMMDeviceEnumerator)

        EDataFlow_eRender   = 0
        ERole_eConsole      = 0

        pDevice = pMde.GetDefaultAudioEndpoint(EDataFlow_eRender, ERole_eConsole)

        CLSCTX_ALL  = 0x17

        iid = GUID('{5CDF2C82-841E-4546-9722-0CF74078229A}')
        pEndPoint   = pDevice.Activate(byref(iid), CLSCTX_ALL, None)
        self.__pEndPoint    = pEndPoint

    def mastervol_up(self):
        self.__pEndPoint.VolumeStepUp(None)

    def mastervol_down(self):
        self.__pEndPoint.VolumeStepDown(None)

    @property
    def mastervol(self):
        return self.__pEndPoint.GetMasterVolumeLevelScalar()

    @mastervol.setter
    def mastervol(self, vol):
        print vol
        self.__pEndPoint.SetMasterVolumeLevelScalar(vol, None)