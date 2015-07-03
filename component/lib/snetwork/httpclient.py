import urllib2

def get(url,timeout=5):
    rtn = ''
    try:
        response = urllib2.urlopen(str(url),timeout=timeout)
        rtn = response.read()
    except:
        pass
    return rtn