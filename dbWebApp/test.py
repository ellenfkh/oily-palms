from requests import put, get
from geopy.distance import vincenty
if __name__ == '__main__':
    put('http://localhost:5050/admin', data={'phoneNumber': 1,
        'latitude':41.49008, 'longitude': -71.312796} ).json()

    put('http://localhost:5050/admin', data={'phoneNumber': 2,
        'latitude':41.499498, 'longitude': -81.695391} ).json()


    print get('http://localhost:5050/admin', data={'phoneNumber': 1} ).json()
    print get('http://localhost:5050/nearby', data={
        'latitude':41.499498, 'longitude': -81.695391, 'radiusInMiles': 5050} ).json()

            
    # test locations from geopy
    # newport_ri = (41.49008, -71.312796)
    # cleveland_oh = (41.499498, -81.695391)


