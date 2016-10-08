import json
from flask import Response

## utility structs (row schemas)
class Coordinates:
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude

class Incident:
    def __init__(self, incidentId, location, time, description):
        self.location = Coordinates(latitude, longitude)
        self.time = time
        self.incidentId = incidentId
        self.description = description

## format a phone nunber -> coordinate entry in json
def formatPhoneEntry(phoneNumber, coordinates):
    js = json.dumps( {"phoneNumber": phoneNumber, "latitude":
        coordinates.latitude, "longitude":
        coordinates.longitude })
    resp = Response(js, status=200, mimetype='application/json')
    return resp

## for testing and proof of concept. In-memory db table.
class Table:

    def __init__(self, debug=True):
        self.debug = debug
        self.table = dict()

    def __getitem__(self, key):
        value = self.table[key]
        return value

    def __setitem__(self, key, value):
        self.table[key] = value

