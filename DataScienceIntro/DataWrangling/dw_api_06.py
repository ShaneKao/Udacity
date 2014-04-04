#!/usr/bin/python

import json
import requests
from pprint import pprint


def api_get_request(url):
    # In this exercise, you want to call the last.fm API to get a list of the
    # top artists in Spain.
    #
    # Once you've done this, return the name of the number 1 top artist in Spain
    #print "url is " + url
    data = requests.get(url).text
    data = json.loads(data)
    #print type(data)
    #print data
    #print "****"
    pprint(data['topartists']['artist'][0]['name'])
    return data['topartists']['artist'][0]['name']
    #return data["topartists"]['artist'][0]
    #return  # return the top artist in Spain



params = {
    "method": "geo.gettopartists",
    "country": "spain",
    "api_key": "my_api_key",
    "format": "json",
}
r = requests.get("http://ws.audioscrobbler.com/2.0/", params=params)

r.raise_for_status()
data = r.json()
pprint(data)