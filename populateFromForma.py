import requests
import datetime
import mysql.connector
from mysql.connector import Error 

r = requests.get('http://gis-gfw.wri.org/arcgis/rest/services/forest_change/MapServer/3/query?where=date%3D%272008-03-21%27&text=&objectIds=&time=&geometry=&geometryType=esriGeometryPoint&inSR=&spatialRel=esriSpatialRelIntersects&relationParam=&outFields=lat%2Clon&returnGeometry=false&returnTrueCurves=false&maxAllowableOffset=&geometryPrecision=&outSR=&returnIdsOnly=false&returnCountOnly=false&f=pjson')
requestJson = r.json()
latLongPairs = []
for problematicTransect in requestJson["features"]:
  latLongPairs.append(problematicTransect["attributes"])

#print latLongPairs


def query_db(query, args):
    ret = []
    print query
    print args
    try:
        conn = mysql.connector.connect(host='127.0.0.1',
                                       db='oily-palm',
                                       user='root',
                                       password='vm4mAeCrP78w')
        if conn.is_connected():
            cursor = conn.cursor()
            cursor.callproc(query, args)
            ret = [row for row in cursor]

        for result in cursor.stored_results():
            print result.fetchall()
        conn.commit()
            
    except Error as e:
        print(e)

    finally:
        conn.close()

    return ret

for pair in latLongPairs:
    print "calling insert forma event: \"{}\", {}, {}".format( 
            datetime.date(2008, 3, 21), 
                pair["lat"],
		pair["lon"])

    # result = query_db("dummy", ())


    result = query_db("insertFormaEvent", ("2008-03-21", 
                pair["lat"],
		pair["lon"] ))

    print result
