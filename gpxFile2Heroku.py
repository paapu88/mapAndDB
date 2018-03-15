""" 
read in a gpx file and push the data into heroku database for 
android app: Google Play MapAndTrack

EXAMPLE1:
python3 gpxFile2Heroku.py ./trackfiles/mattby1.gps --name mattby

EXAMPLE2:
python3 gpxFile2Heroku.py ./trackfiles/porkkala.gps --name porkkala --date 20180401 

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

today = datetime.datetime.today().strftime('%Y%m%d')

parser = argparse.ArgumentParser(description='Put gpx-datafile information to database')
parser.add_argument('filename', help='Name of the file containing gpx data')
parser.add_argument('--http', default='https://map-and-db.herokuapp.com/track/', help='www adress of the database')
parser.add_argument('--name', default='suunnistus', help='name-tag for the o-course/ gps track')
parser.add_argument('--date', default=today, help='date for the event, use format YYYYMMDD', type=lambda d: datetime.datetime.strptime(d, '%Y%m%d'))
args = parser.parse_args()


lines = [line.rstrip('\n').strip() for line in open(args.filename)]

oklines = ""
for line in lines:
    if ('<trkpt lat=' in line):
        lat = line.split()[1]
        lon = line.split()[2]
        lat1 = re.findall(r'"([^"]*)"', lat)
        lon1 = re.findall(r'"([^"]*)"', lon)
        #lat2 = lat1[0].strip('\'')
        #lon2 = lon1[0].strip('\'')
        #print(lat2, lon2)
        oklines = oklines + lat1[0]+" " +lon1[0]+" "

myjson = {'date':args.date.strftime('%Y%m%d'), 'track': oklines[:-1]}
print(myjson)
#print(myjson.replace("\'","\""))

print("ADDRESS:"+args.http+args.name)

url = args.http + args.name # Set destination URL here
request = Request(url, urlencode(myjson).encode())
json = urlopen(request).read().decode()
print(json)

#r = requests.post(, data=myjson)
#print(r.status_code, r.reason)




