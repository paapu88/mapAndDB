"""


read in a gpx file and push the data into google firebase

EXAMPLE1:
python gpxFile2Firebase.py ./trackfiles/mattby1.gps --name mattby

see https://towardsdatascience.com/nosql-on-the-cloud-with-python-55a1383752fc

EXAMPLE2:
python gpxFile2Firebase.py ./trackfiles/porkkala.gps --name porkkala --date 20180401

"""
import sys, re
from pprint import pprint
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import argparse
import datetime
#from flask import jsonify, json
from flask import jsonify, json
import datetime
from geopy import distance
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore




today = datetime.datetime.today().strftime('%Y%m%d')

parser = argparse.ArgumentParser(description='Put gpx-datafile information to database')
parser.add_argument('filename', help='Name of the file containing gpx data')
parser.add_argument('--http', default='https://map-and-db.herokuapp.com/track/', help='www adress of the database')
parser.add_argument('--name', default='suunnistus', help='name-tag for the o-course/ gps track')
parser.add_argument('--date', default=today, help='date for the event, use format YYYYMMDD', type=lambda d: datetime.datetime.strptime(d, '%Y%m%d'))
args = parser.parse_args()


lines = [line.rstrip('\n').strip() for line in open(args.filename)]

lats = []
lons=[]
for line in lines:
    if ('<trkpt lat=' in line):
        lat = line.split()[1]
        lon = line.split()[2]
        lat1 = re.findall(r'"([^"]*)"', lat)
        lon1 = re.findall(r'"([^"]*)"', lon)
        lats.append(round(float(lat1[0]),6))
        lons.append(round(float(lon1[0]),6))

# get length of the course
oldlat=None
oldLon=None
d=0.0
for lat, lon in zip(lats, lons):
    if oldlat is None:
        oldlat=lat
        oldLon=lon
        continue
    point0=(lat, lon,0.0)
    point1=(oldlat, oldLon,0.0)
    print(point0)
    print(point1)
    d += distance.distance(point0, point1).km
    oldlat=lat
    oldLon=lon
    print(lat, lon, d)
coursename = args.date.strftime('%Y%m%d')+'_'+args.name
data = {'lats':lats, 'lons':lons,'nofcontrols':len(lats), 'dist':round(d,2),
             'runners':[]}
jsondata = json.dumps(data, indent = 4)
print(jsondata)

# Use a service account
cred = credentials.Certificate('./data/esuunnistus-firebase-adminsdk-hg9nn-df2ae8203a.json')
#credentials.Certificate('path/to/serviceAccount.json')
firebase_admin.initialize_app(cred)
db = firestore.client()  # this connects to our Firestore database
collection = db.collection('courses')  # opens 'places' collection
res = collection.document(coursename).set(data)
print(res)


sys.exit()
print("ADDRESS:"+args.http+args.name)

url = args.http + args.name # Set destination URL here
request = Request(url, urlencode(myjson).encode())
json = urlopen(request).read().decode()
print(json)

#r = requests.post(, data=myjson)
#print(r.status_code, r.reason)




