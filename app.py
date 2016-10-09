from flask import Flask, request, Response, render_template
import requests
import json
from twilio.rest import TwilioRestClient
from twilio import twiml
import credentials
import mysql.connector
from mysql.connector import Error 
import datetime

account_sid = credentials.login['sid']
auth_token = credentials.login['token']

app = Flask(__name__)

@app.route('/')
def hello_world():
    # FORMA data
    r = requests.get('http://gis-gfw.wri.org/arcgis/rest/services/forest_change/MapServer/3/query?where=date%3D%272008-03-21%27&text=&objectIds=&time=&geometry=&geometryType=esriGeometryPoint&inSR=&spatialRel=esriSpatialRelIntersects&relationParam=&outFields=lat%2Clon&returnGeometry=false&returnTrueCurves=false&maxAllowableOffset=&geometryPrecision=&outSR=&returnIdsOnly=false&returnCountOnly=false&f=pjson')
    requestJson = r.json()
    latLongPairs = []
    for problematicTransect in requestJson["features"]:
      latLongPairs.append(problematicTransect["attributes"])

    # Find cellphone numbers with x threshold distance for each lat long pair
    phone_numbers = query_db("call getPhonesByDate(\"%s\")" % str(datetime.date(2008, 3, 21)), ())
    
    # Dedupe
    phone_numbers = set(phone_numbers)

    # Loop over numbers and send messages
    for phone_number in phone_numbers:
      print(phone_number)
      client = TwilioRestClient(account_sid, auth_token)
     
      client.messages.create(
         to=phone_number,
         from_="+13106834844",
         body="A deforestation incident was reported within five kilometers of your home. Are you aware of this incident? Reply 'yes' or 'no'."
      ) 
    return 'Hello World!'

@app.route('/incidents')
def show_incidents():
    #incidents = query_db("SELECT * from incident JOIN events ON incident.event=events.event", ())
    incidents = [(1, 1, 1, 1, 1)]
    return render_template("incidents.html",  incidents=incidents)

@app.route('/twilio', methods=['POST'])
def inbound_sms():
    response = twiml.Response()
    inbound_message = request.form.get("Body")
    phone_number = request.form.get("From")
    # Get incident using phone number
    eventId = "1234"

    if (inbound_message.lower()== "yes"):
        responseString = "What type of incident occurred? "
        responseString += "Reply '1' for intentional fire, "
        responseString += "'2' for naturally caused fire, "
        responseString += "'3' for fire with unknown cause, "
        responseString += "'4' for logging."
        response.message(responseString)

    elif (inbound_message == "1"):
        # Write BAD fire to database
        query_db("INSERT into incident values({}, {}, {}, 1)".format(eventId, datetime.datetime.now(), eventId))
        response.message("Thank you for your assistance. Reported intentional fire.")
    elif (inbound_message == "2"):
        # Write NATURAL fire
        query_db("INSERT into incident values({}, {}, {}, 2)".format(eventId, datetime.datetime.now(), eventId))
        response.message("Thank you for your assistance. Reported natural fire.")
    elif (inbound_message == "3"):
        # Write MYSTERY fire
        query_db("INSERT into incident values({}, {}, {}, 3)".format(eventId, datetime.datetime.now(), eventId))
        response.message("Thank you for your assistance. Reported MYSTERY fire.")
    elif (inbound_message == "4"):
        # Write MYSTERY fire
        query_db("INSERT into incident values({}, {}, {}, 4)".format(eventId, datetime.datetime.now(), eventId))
        response.message("Thank you for your assistance. Reported logging.")
    else:
        # FIXME: continue nagging
        response.message("Unknown code. Please try again.")
    
    return Response(str(response), mimetype="application/xml"), 200

def callproc_db(procedure, args):
    ret = []
    try:
        conn = mysql.connector.connect(host='127.0.0.1',
                                       db='oily-palm',
                                       user='root',
                                       password='vm4mAeCrP78w')
        if conn.is_connected():
            cursor = conn.cursor()
            cursor.callproc(procedure, args)

            finalResult = []
            for result in cursor.stored_results():
                finalResult.append(result.fetchall())
            
    except Error as e:
        print(e)

    finally:
        conn.close()

    return ret

def query_db(query, args):
    ret = []
    try:
        conn = mysql.connector.connect(host='127.0.0.1',
                                       db='oily-palm',
                                       user='root',
                                       password='vm4mAeCrP78w')
        if conn.is_connected():
            cursor = conn.cursor()
            cursor.execute(query, args)
            ret = [row for row in cursor]

            finalResult = []
            for result in cursor.stored_results():
                finalResult.append(result.fetchall())
               
    except Error as e:
        print(e)

    finally:
        conn.close()

    return ret


if __name__ == '__main__':
    app.run(debug=True)
