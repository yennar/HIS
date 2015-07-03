import pyaudio
import wave
import sys

_CHUNK = 1024

def play_wave(filename):
    wf = wave.open(filename, 'rb')
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)
    
    data = wf.readframes(_CHUNK)
    while data != '':
        stream.write(data)
        data = wf.readframes(_CHUNK)
    stream.stop_stream()
    stream.close()
    
    p.terminate()    