#!python3

#import appex, ui

#Lat/Lon Calc
from math import cos, asin, sqrt

# XML fetch and parse
import urllib.request, urllib.error, urllib.parse
from io import StringIO
from io import BytesIO
import gzip
import untangle

#GPS Data
#import location

#Sleep
import time

#clear Console
import console


def distance(lat1, lon1, lat2, lon2):
   p = 0.017453292519943295
   a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p)*cos(lat2*p) * (1-cos((lon2-lon1)*p)) / 2
   return 12742 * asin(sqrt(a))

def closest(data, v):
   return min(data, key=lambda p: distance(v['lat'],v['lon'],p['lat'],p['lon']))


def getMNDOTData():
	request = urllib.request.Request('http://data.dot.state.mn.us/iris_xml/det_sample.xml.gz')
	request.add_header('Accept-encoding', 'gzip')
	response = urllib.request.urlopen(request)
	buf = BytesIO(response.read())
	f = gzip.GzipFile(fileobj=buf)
	sensorXML = f.read()

	return sensorXML

def getTravelPath():
	eastBound = [{'lat': 44.97102, 'lon': -93.49132, 'station': "S266", 'L1': "1635", 'L2': "1636", 'L3': "1637"},
	             {'lat': 44.97087, 'lon': -93.47491, 'station': "S267", 'L1': "1641", 'L2': "1642", 'L3': "1643"},
	             {'lat': 44.97085, 'lon': -93.46664, 'station': "S268", 'L1': "1645", 'L2': "1646", 'L3': "1647"},
	             {'lat': 44.97083, 'lon': -93.45459, 'station': "S269", 'L1': "1651", 'L2': "1652", 'L3': "1653"},
	             {'lat': 44.97082, 'lon': -93.44299, 'station': "S270", 'L1': "1656", 'L2': "1657", 'L3': "5447"},
	             {'lat': 44.97084, 'lon': -93.43139, 'station': "S271", 'L1': "1661", 'L2': "1662", 'L3': "5448"},
	             {'lat': 44.97114, 'lon': -93.41901, 'station': "S272", 'L1': "1669", 'L2': "1670"},
	             {'lat': 44.973, 'lon': -93.40945, 'station': "S273", 'L1': "1676", 'L2': "1678"},
	             {'lat': 44.97325, 'lon': -93.40179, 'station': "S274", 'L1': "1682", 'L2': "1683"},
	             {'lat': 44.9738, 'lon': -93.3891, 'station': "S275", 'L1': "1686", 'L2': "1687"},
	             {'lat': 44.97205, 'lon': -93.38244, 'station': "S276", 'L1': "1693", 'L2': "1694", 'L3': "1695"},
	             {'lat': 44.97115, 'lon': -93.3726, 'station': "S277", 'L1': "1698", 'L2': "1699"},
	             {'lat': 44.97095, 'lon': -93.36201, 'station': "S278", 'L1': "1703", 'L2': "1704"},
	             {'lat': 44.97034, 'lon': -93.35173, 'station': "S279", 'L1': "1708", 'L2': "1709"},
	             {'lat': 44.97048, 'lon': -93.34354, 'station': "S280", 'L1': "1712", 'L2': "1713"},
	             {'lat': 44.9703, 'lon': -93.3363, 'station': "S281", 'L1': "1719", 'L2': "1720", 'L3': "1721"},
	             {'lat': 44.97039, 'lon': -93.31963, 'station': "S282", 'L1': "1730", 'L2': "1731", 'L3': "1732"},
	             {'lat': 44.97017, 'lon': -93.3197, 'station': "S284", 'L1': "793", 'L2': "794", 'L2': "794"},
	             {'lat': 44.96977, 'lon': -93.30786, 'station': "S286", 'L1': "783", 'L2': "784", 'L3': "785"},
	             {'lat': 44.96946, 'lon': -93.30118, 'station': "S288", 'L1': "1737", 'L2': "770", 'L3': "771",'L4': "772"},
	             {'lat': 44.97484, 'lon': -93.28936, 'station': "S290", 'L1': "673", 'L2': "674"},
	             {'lat': 44.97527, 'lon': -93.28338, 'station': "S291", 'L1': "611", 'L2': "701", 'L3': "702"}]

	westBound = []

	return eastBound

console.clear()

while True:
	
	#Fetch Phone's GPS Location
	#print("Pythonista")
	
	#Turn GPS updating on phone
	#location.start_updates()
	#myLocation = location.get_location()
	#location.stop_updates()
	
	#print(myLocation['longitude'])
	#print(myLocation['latitude'])
	myLocation = {'latitude': 44.970902, 'longitude': -93.443801}
	
	#Values for finding station closest to current lat/lon
	v = {'lat': myLocation['latitude'], 'lon': myLocation['longitude']}
	
	
	#Store closest location to current GPS
	closestStation = closest(getTravelPath(), v)['station']
	#print(closestStation)
	
	#Load sensor data from MN website
	
	latestSensorData = untangle.parse(str(getMNDOTData(), 'utf-8')).traffic_sample.sample
	
	#Count number of lanes displayed
	laneDisplayCount = 0
	
	#Loop on all stations to get best lane for each station
	for stationlist in getTravelPath():
		#print(stationlist)
	
		speeds=[]
		lane=[]
		
		#load stations into dictionary to itterate on. 
		stationDetails = dict(stationlist)
		
		#Loop on each sensor in MN output
		for sensors in latestSensorData:
	
			#Loop on current station to check each lane in station against current sensor
			for k, v in list(stationDetails.items()):
	
				#If a match is found for the station append to array for current station and speed			
				if sensors['sensor'] == v:
					if sensors['speed'] == "UNKNOWN":
						speeds.append(100)
						lane.append(k)
					else:
						speeds.append(int(sensors['speed']))
						lane.append(k)
							
					#print(sensors['sensor'])
					#print(sensors['speed'])
		#print(speeds)
		#print(max(speeds))
	
	
		if len(speeds)>0:
			print("%s Lane: %s is at %s" % (stationlist['station'],lane[speeds.index(max(speeds))],max(speeds)))
		else:
			print("%s has no data" % (stationlist['station']))


	#Sleep for 30 seconds and check it all again
	time.sleep (30)		