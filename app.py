from flask import Flask, request, Response
import requests
import json
from twilio.rest import TwilioRestClient
from twilio import twiml
import credentials
import mysql.connector
from mysql.connector import Error 

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

    print latLongPairs
    # Find cellphone numbers with x threshold distance for each lat long pair
    
    try:
        conn = mysql.connector.connect(host='localhost',
                                       database='python_mysql',
                                       user='root',
                                       password='vm4mAeCrP78w')
        if conn.is_connected():
            print('Connected to MySQL database')
 
    except Error as e:
        print(e)
 
    #finally:
        #conn.close()


    # Dedupe
    # Loop over numbers and send messages

    client = TwilioRestClient(account_sid, auth_token)
 
    
   # client.messages.create(
   #    to="+12142548650",
   #    from_="+13106834844",
   #    body="A deforestation incident was reported within five kilometers of your home. Are you aware of this incident? Reply 'yes' or 'no'."
   # ) 
    return 'Hello World!'

@app.route('/twilio', methods=['POST'])
def inbound_sms():
    response = twiml.Response()
    inbound_message = request.form.get("Body")
    phone_number = request.form.get("From")
    # Get incident using phone number

    if (inbound_message == "yes"):
        response.message("What type of incident occurred? Reply '1' for intentional fire, '2' for naturally caused fire, '3' for logging.")
    elif (inbound_message == "1"):
        # Write BAD fire to database
	response.message("Thank you for your assistance.")
    elif (inbound_message == "2"):
        # Write NATURAL fire
	response.message("Thank you for your assistance.")
    elif (inbound_message == "3"):
	response.message("Thank you for your assistance.")
    
    return Response(str(response), mimetype="application/xml"), 200

if __name__ == '__main__':
    app.run(debug=True)
