import requests
import json


class Ziga(object):
    def __init__(self, applicationKey, host, port=80, protocol='http'):
        self.app_key = applicationKey
        self.protocol = protocol
        self.host = host
        self.port = port


class Channel(object):
    def __init__(self, ziga_obj, channel_name):
        self.ziga_obj = ziga_obj
        self.channel_name = channel_name
        self.url = '{4}://{0}:{1}/{2}/{3}/'.format(self.ziga_obj.host,
                                                    self.ziga_obj.port,
                                                    self.ziga_obj.app_key,
                                                    self.channel_name,
                                                    self.ziga_obj.protocol)

    def trigger(self, event, data={}):
        to_post = {'event': event, 'data': data}
        headers = {'Content-type': 'application/json'}
        response = requests.post(self.url,
                                data=json.dumps(to_post),
                                headers=headers)
        #TODO: handle response codes here

    def authenticate(self):
        headers = {'Content-type': 'application/json'}
        response = requests.post(self.url, data='{}', headers=headers)
        return r.text
