# read in a gpx file and change the coodinates to json
# python3 gpxFile2Json.py ~/Downloads/pullautuskartta1244447522.gpx

import sys, re
from pprint import pprint

import datetime
#from flask import jsonify, json


from flask import jsonify, json
import datetime


lines = [line.rstrip('\n').strip() for line in open(sys.argv[1])]

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


mydate = datetime.datetime.today().strftime('%Y%m%d')
myjson = "{"+'"date":"'+mydate+'", "track":'+'"'+ oklines[:-1]+'"}'
print(myjson)

today = datetime.datetime.today().strftime('%Y%m%d')

myjson = "{"+"\"date\":\""+today+"\", \"track\":\""+ oklines[:-1]+'"}'
print(myjson.replace("\'","\""))


