
import snetwork.httpclient as httpclient
import snetwork.httputils as httputils
import os
import json
import argparse
import time
from log.log import *
import urllib

this_path = os.path.dirname(os.path.realpath(__file__))
warning_file = this_path + '/share/warning.wav'

parser = argparse.ArgumentParser(prog='HTTP_SERVER')
parser.add_argument('-t', '--threadhold',default='40',type=int)
result = parser.parse_args()

temperature_device = httputils.find_lan_device('b318fd7f-5182-4662-8691-a68fbfbaf182')
if temperature_device is None:
    print_error("Cannot find temperature_device")
    exit(1)

voice_device = httputils.find_lan_device('79064f23-57cc-43ca-8fcc-dee7f886fb6e')
if voice_device is None:
    print_error("Cannot find voice_device")
    exit(1)
    
speed_low = 2
speed_low_i = 60
speed_high_c = 20

voice_flag = 0
temperature_db = {}

safe_counter = speed_high_c

while True:
    temperature_sensor_data = json.loads(httpclient.get('http://%s:%d/data' % (temperature_device.address,temperature_device.port)))
    temperature_now = temperature_sensor_data['data']
    temperature_ts  = temperature_sensor_data['time']
    
    temperature_low = temperature_now - speed_low
    if temperature_low in temperature_db.keys():
        if temperature_ts - temperature_db[temperature_low] < speed_low_i:
            print_info("temperature %d increase fast" % temperature_now)
            voice_flag = 1

    if temperature_now >= result.threadhold:
        print_info("temperature %d over threadhold" % temperature_now)
        voice_flag = 1
        
    if temperature_now < result.threadhold:
        safe_counter = safe_counter - 1
    else:
        safe_counter = speed_high_c

    if safe_counter == 0:
        print_info("temperature %d safe" % temperature_now)
        voice_flag = 0
    
    if voice_flag:
        voice_string = "Warning! Temperature over threadhold. %d degrees Celsius" % temperature_now
        httpclient.get('http://%s:%d/say?content=%s' % (voice_device.address,voice_device.port,urllib.quote(voice_string)),timeout=20)
        time.sleep(5)
    time.sleep(5)
    temperature_db[temperature_now] = temperature_ts
