from requests import put, get
if __name__ == '__main__':
    put('http://localhost:5000/admin', data={'phoneNumber': 12345,
        'latitude':1, 'longitude':2 } ).json()

    print get('http://localhost:5000/admin', data={'phoneNumber': 12345} ).json()
