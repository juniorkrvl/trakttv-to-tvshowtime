import requests, json, urllib, sys, time, ConfigParser
from datetime import datetime, timedelta

class Trakt(object):

    def is_token_valid(self):
        parser = ConfigParser.ConfigParser()
        parser.read('config.ini')
        
        valid = False
        access_token = parser.get('trakt','access_token')
        expiration_date = parser.get('trakt','expiration_date')

        if len(expiration_date) > 0 and datetime.now() < datetime.strptime(expiration_date, "%Y-%m-%d"):
            valid = True

        if len(access_token) > 0:
            valid = True        

        return valid


    def auth(self):      
        parser = ConfigParser.ConfigParser()
        parser.read('config.ini')
        #a + datetime.timedelta(seconds=3)

        params = {'client_id':'2e822b8d7347e790b792f64bba6bbdc8caebe5005c6ac76ce7920c65ae878eed'}
        headers = {'Content-Type': 'application/json'}
        url = 'https://api.trakt.tv/oauth/device/code?%s' % urllib.urlencode(params)
        r = requests.post(url,headers=headers)
        obj = json.loads(r.content)
        
        raw_input("Please, insert the code {user_code} on {verification_url}. Press any key if you are ready...".format(**obj))

        params = {
            'code': obj['device_code'],
            'client_id': '2e822b8d7347e790b792f64bba6bbdc8caebe5005c6ac76ce7920c65ae878eed',
            'client_secret': '4f0dcb8c483cd7d2d9d53c651d64a0d29d14fa8e68355315d6300a8396c4b76d'
            }
        url = 'https://api.trakt.tv/oauth/device/token'
        r = requests.post(url,data=json.dumps(params),headers=headers)

        token = json.loads(r.content)

        print token
        parser.set('trakt','access_token',token['access_token'])
        parser.set('trakt','refresh_token',token['refresh_token'])

        expiration_date = datetime.now() + timedelta(seconds=token['expires_in'])
        parser.set('trakt','expiration_date',expiration_date.strftime("%Y-%m-%d"))

        with open('config.ini', 'wb') as configfile:
            parser.write(configfile)
        
        print "You're all set!"


    def get_history(self):
        parser = ConfigParser.ConfigParser()
        parser.read('config.ini')
        
        access_token = parser.get('trakt','access_token')
        client_id = parser.get('trakt','client_id')
        username = parser.get('trakt','username')

        from_date = (datetime.now() - timedelta(minutes=70)).strftime("%Y-%m-%dT%H:%M:00.000Z")
        to_date = datetime.now().strftime("%Y-%m-%dT%H:%M:00.000Z")

        #2016-06-01T00:00:00.000Z

        params = {'type':'episodes', 'start_at':from_date,'end_at':to_date}
        headers = {'Content-Type': 'application/json', 'trakt-api-version':'2', 'trakt-api-key':client_id}
        url = 'https://api.trakt.tv/users/' + username + '/history/episodes?%s' % urllib.urlencode(params)
        r = requests.get(url,headers=headers)
        obj = json.loads(r.content)

        return obj
        

    def add_to_watchlist(self,array_shows):
        parser = ConfigParser.ConfigParser()
        parser.read('config.ini')
        
        access_token = parser.get('trakt','access_token')
        client_id = parser.get('trakt','client_id')
        username = parser.get('trakt','username')

        headers = {'Content-Type': 'application/json', 'Authorization':'Bearer %s' % access_token, 'trakt-api-version':'2', 'trakt-api-key':client_id}
        url = 'https://api.trakt.tv/sync/watchlist'
        r = requests.post(url,data=json.dumps(array_shows),headers=headers)
        obj = json.loads(r.content)

        return obj

        

if __name__ == '__main__':
    t = Trakt()
    t.auth()

