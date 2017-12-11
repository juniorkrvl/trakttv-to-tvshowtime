import requests, json, urllib, sys, time, ConfigParser
from datetime import datetime, timedelta

class TVShowTime(object):

    def __init__(self):
        parser = ConfigParser.ConfigParser()
        parser.read('config.ini')

        self.username = parser.get('tvshowtime','username')
        self.password = parser.get('tvshowtime','password')

    def to_watch(self):
        r = requests.get('https://api.tvshowtime.com/v1/to_watch', auth=(self.username, self.password))
        obj = json.loads(r.content)

        return obj

    def save_progress(self, shows_array):
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        r = requests.post('https://api.tvshowtime.com/v1/show_progress',data="shows="+json.dumps(shows_array), auth=(self.username, self.password), headers=headers)
        obj = json.loads(r.content)

        return obj