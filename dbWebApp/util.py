import json
from flask import Response
from geopy.distance import vincenty

## utility structs (row schemas)

class Incident:
    def __init__(self, incidentId, location, time, description):
        self.location = (latitude, longitude)
        self.time = time
        self.incidentId = incidentId
        self.description = description

## format a phone nunber -> coordinate entry in json
def formatPhoneEntry(phoneNumber, coordinates):
    js = json.dumps( {"phoneNumber": phoneNumber, "latitude":
        coordinates[0], "longitude":
        coordinates[1]})
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


class PhoneBook(Table):

    ## FIXME not at all scalable. plz fix
    def getByLocation(self, location, radiusInMiles):
        nearby = dict()
        for key, value in self.table.iteritems():
            if (vincenty(location, value).miles < radiusInMiles):
                nearby[key] = value

        return nearby;
