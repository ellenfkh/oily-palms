from flask import Flask, request
from flask import Response
from flask_restful import Resource, Api
from util import Table, PhoneBook, Incident, formatPhoneEntry
from datetime import datetime
import json

app = Flask(__name__)
api = Api(app)

# FIXME not thread safe, just kind of awful
incidentIdCounter = 1
incidents = Table(True)
phoneTable = PhoneBook(True)

class Phone(Resource):
    def get(self):
        phoneNumber = request.form['phoneNumber']
        return formatPhoneEntry(phoneNumber, phoneTable[phoneNumber] )

    def put(self):
        phoneNumber = request.form['phoneNumber']
        latitude = request.form['latitude']
        longitude = request.form['longitude']
        phoneTable[phoneNumber] = (latitude, longitude)

class LocationQuery(Resource):
    def get(self):
        latitude = request.form['latitude']
        longitude  = request.form['longitude']
        radius  = request.form['radiusInMiles']
        return phoneTable.getByLocation((latitude, longitude), int(radius))

class Incidents(Resource):
    def get(self):
        incidentId = request.form["incidentId"]
        return incidents[incidentId]

    def put(self, latitude, longitude, descrption):
        incidentIdCounter +=1
        latitude = request.form['latitude']
        longitude  = request.form['longitude']
        description  = request.form['description']
        incidents[incidentIdCounter] = Incident((latitude,
            longitude), utcnow(), description)
        return incidentIdCounter

class Index(Resource):
    def get(self):
        return {'fixme': 'PUT A NICE PICTURE HERE'}


api.add_resource(Index, '/')
api.add_resource(Phone, '/admin')
api.add_resource(LocationQuery, '/nearby')
api.add_resource(Incidents, '/reporting')

if __name__ == '__main__':
    app.run(debug=True, port=5050)

