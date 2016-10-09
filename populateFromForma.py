import requests
import datetime

r = requests.get('http://gis-gfw.wri.org/arcgis/rest/services/forest_change/MapServer/3/query?where=date%3D%272008-03-21%27&text=&objectIds=&time=&geometry=&geometryType=esriGeometryPoint&inSR=&spatialRel=esriSpatialRelIntersects&relationParam=&outFields=lat%2Clon&returnGeometry=false&returnTrueCurves=false&maxAllowableOffset=&geometryPrecision=&outSR=&returnIdsOnly=false&returnCountOnly=false&f=pjson')
requestJson = r.json()
latLongPairs = []
for problematicTransect in requestJson["features"]:
  latLongPairs.append(problematicTransect["attributes"])

print latLongPairs


try:
    conn = mysql.connector.connect(host='127.0.0.1',
                                   db='oily-palm',
                                   user='root',
                                   password='vm4mAeCrP78w')
    if conn.is_connected():
        print('Connected to MySQL database')

    cursor = conn.cursor();

    for pair in latLongPairs:
        cursur.callproc("insertFormaEvent",
                datetime.datetime(2008, 3, 21).date(),
                pair[lat],
                pair[lon] )

except Error as e:
    print(e)

finally:
    conn.close()
