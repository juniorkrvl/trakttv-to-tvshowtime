from urllib2 import Request, urlopen
import json
import requests

class Requester(object):
    
    def __init__(self):
        pass
    
    def get(self, url, data={}, headers={}):
        r = requests.get(url, params=json.dumps(data), headers=headers)
        

        request = Request(url, data=data, headers=headers)
        response_body = urlopen(request).read()

        obj = json.loads(response_body)

        return obj

    