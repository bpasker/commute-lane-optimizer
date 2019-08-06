#!python3

#UI for Pythonista
import appex, ui

#Lat/Lon Calc
from math import cos, asin, sqrt, radians, sin, atan2, degrees

# XML fetch and parse
import urllib.request, urllib.error, urllib.parse
from io import StringIO
from io import BytesIO
import gzip
import untangle

#GPS Data
import location

#Sleep
import time

#clear Console
import console

#Speech
import speech
import sound

#check current os
import platform


#Global Variables
#previousGPS = (44.97102,-93.49132)
#currentGPS = (44.97087,-93.47491)

def distance(lat1, lon1, lat2, lon2):
   p = 0.017453292519943295
   a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p)*cos(lat2*p) * (1-cos((lon2-lon1)*p)) / 2
   return 12742 * asin(sqrt(a))

def closest(data, v):
   return min(data, key=lambda p: distance(v['lat'],v['lon'],p['lat'],p['lon']))

def getMNDOTData():
	request = urllib.request.Request('http://data.dot.state.mn.us/iris_xml/det_sample.xml.gz')
	request.add_header('Accept-encoding', 'gzip')
	
	#Try to get the latest XML 
	for i in range(5):	
		while True:
			try:
				response = urllib.request.urlopen(request)
			except urllib.URLError:
				continue
			break
					        
	buf = BytesIO(response.read())
	f = gzip.GzipFile(fileobj=buf)
	sensorXML = f.read()

	return sensorXML
	
def voiceUpdate(laneVoice,speedsVoice,lastLaneVoice,slowDown):
	
	sound.set_honors_silent_switch(False)

	if slowDown == 0:	
		if lastLaneVoice != laneVoice[speedsVoice.index(max(speedsVoice))]:	
			if voice.value == 1:
				speech.say("Switch to lane %s" % (laneVoice[speedsVoice.index(max(speedsVoice))])[-1])
			else:
				for i in range(int(laneVoice[speedsVoice.index(max(speedsVoice))][-1])):
					sound.play_effect('Coin_2',1)
					time.sleep(.3)
	else:
		if voice.value == 1:
			speech.say("Prepare for a major slowdown and move to lane %s" % (lane[speeds.index(max(speeds))][-1]))
		else:
			sound.play_effect('Ding_3',1)
			time.sleep(.5)
			for i in range(int(laneVoice[speedsVoice.index(max(speedsVoice))][-1])):
					sound.play_effect('Coin_2',1)
					time.sleep(.3)
					eventLog.text = str(slowDown)

def calculate_initial_compass_bearing(pointA, pointB):
    if (type(pointA) != tuple) or (type(pointB) != tuple):
        raise TypeError("Only tuples are supported as arguments")

    lat1 = radians(pointA[0])
    lat2 = radians(pointB[0])

    diffLong = radians(pointB[1] - pointA[1])

    x = sin(diffLong) * cos(lat2)
    y = cos(lat1) * sin(lat2) - (sin(lat1)
            * cos(lat2) * cos(diffLong))

    initial_bearing = atan2(x, y)

    initial_bearing = degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360
    
    #eventLog.text = str(compass_bearing)

    bearings = ["NE", "E", "SE", "S", "SW", "W", "NW", "N"];

    index = compass_bearing - 22.5
    if index < 0 :
        index += 360
    index = int(index / 45)

    return bearings[index]
			
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

	westBound = [{'lat': 4.97039, 'lon': -93.31963, 'station': "S283", 'L1': "788", 'L2': "789", 'L3': "790"},
				{'lat': 44.97002, 'lon': -93.30761, 'station': "S285", 'L1': "777", 'L2': "778", 'L3': "779"},
				{'lat': 44.96971, 'lon': -93.30132, 'station': "S287", 'L1': "767", 'L2': "768", 'L3': "769"},
				{'lat': 44.97484, 'lon': -93.28936, 'station': "S290", 'L1': "597", 'L2': "598"},
				{'lat': 44.97019, 'lon': -93.32775, 'station': "S318", 'L1': "1740", 'L2': "1741", 'L3': "1742"},
				{'lat': 44.97066, 'lon': -93.33617, 'station': "S319", 'L1': "1722", 'L2': "1723"},
				{'lat': 44.97076, 'lon': -93.34351, 'station': "S320", 'L1': "1750", 'L2': "1751"},
				{'lat': 44.97053, 'lon': -93.35172, 'station': "S321", 'L1': "1754", 'L2': "1755", 'L3': "1756"},
				{'lat': 44.97117, 'lon': -93.36188, 'station': "S336", 'L1': "1760", 'L2': "1761", 'L3': "1762", 'L4': "5458"},
				{'lat': 44.97139, 'lon': -93.37261, 'station': "S337", 'L1': "5848", 'L2': "1765", 'L3': "1766", 'L4': "5459"},
				{'lat': 44.97223, 'lon': -93.38219, 'station': "S338", 'L1': "5849", 'L2': "1771", 'L3': "1772", 'L4': "5460"},
				{'lat': 44.97404, 'lon': -93.3891, 'station': "S339", 'L1': "1776", 'L2': "1777", 'L3': "5461"},
				{'lat': 44.97366, 'lon': -93.3993, 'station': "S340", 'L1': "1780", 'L2': "1781", 'L3': "5462"},
				{'lat': 44.97323, 'lon': -93.40946, 'station': "S341", 'L1': "1787", 'L2': "1788", 'L3': "1789", 'L4': "5463"},
				{'lat': 44.97136, 'lon': -93.41911, 'station': "S342", 'L1': "1792", 'L2': "1793", 'L3': "5464"},
				{'lat': 44.97108, 'lon': -93.43134, 'station': "S343", 'L1': "1797", 'L2': "1798", 'L3': "5465"},
				{'lat': 44.97107, 'lon': -93.44304, 'station': "S344", 'L1': "1801", 'L2': "1802", 'L3': "5466"},
				{'lat': 44.97106, 'lon': -93.45457, 'station': "S345", 'L1': "1806", 'L2': "1807", 'L3': "1808"},
				{'lat': 44.97108, 'lon': -93.4639, 'station': "S346", 'L1': "1811", 'L2': "1812", 'L3': "1813"},
				{'lat': 44.97109, 'lon': -93.47488, 'station': "S347", 'L1': "1820", 'L2': "1821", 'L3': "1822"},
				{'lat': 44.97123, 'lon': -93.49121, 'station': "S348", 'L1': "1825", 'L2': "1826", 'L3': "1827"}]
	

	#Write previous GPS before updating and sleeping.
	try:
		previousGPS
		
		#See if you have moving before it is used to calculate direction
		if distance(previousGPS[0],previousGPS[1],currentGPS[0],currentGPS[1]) > .01:
			
			#Calculate Direction
			myDirection = calculate_initial_compass_bearing(previousGPS,currentGPS)
			
			#Set values based on bearing
			if myDirection in ["NE", "E", "SE"]:
				direction.selected_index = 1
				return eastBound
			elif myDirection in ["SW", "W", "NW"]:
				direction.selected_index = 0
				return westBound
			elif myDirection in ["S"]:
				eventLog.text = "S"
				if direction.selected_index == 0:
					return westBound
				else:
					direction.selected_index = 1
					return eastBound
			elif myDirection in ["N"]: 
				eventLog.text = "N"
				if direction.selected_index == 0:
					return westBound
				else:
					direction.selected_index = 1
					return eastBound
			else:
				eventLog.text = "WTF"
		else:
			if direction.selected_index == 0:
				return westBound
			else:
				direction.selected_index = 1
				return eastBound
			
	except NameError:
		#return data set depending on direction toggle in UI
		if direction.selected_index == 0:
			return westBound
		else:
			direction.selected_index = 1
			return eastBound
			
#Turn screen timout off so phone doesn't sleep
console.set_idle_timer_disabled("disable")


#Buildling out view info.	
v = ui.View(frame=(0, 0, 300, 110))

#Setup 3 labels for each station to write
S1 = ui.Label(frame=(100, 5, 195, 20), flex='lwh', font=('<System>', 16), alignment=ui.ALIGN_LEFT, name='result_label')
S2 = ui.Label(frame=(100, 25, 195, 20), flex='lwh', font=('<System>', 16), alignment=ui.ALIGN_LEFT, name='result_label')
S3 = ui.Label(frame=(100, 45, 195, 20), flex='lwh', font=('<System>', 16), alignment=ui.ALIGN_LEFT, name='result_label')
eventLog = ui.Label(frame=(100, 65, 195, 20), flex='lwh', font=('<System>', 16), alignment=ui.ALIGN_LEFT, name='result_label')
v.add_subview(S1)
v.add_subview(S2)
v.add_subview(S3)
v.add_subview(eventLog)

#Selection control for east/west
direction = ui.SegmentedControl(frame=(5,5,100,50),segments=["West","East"],felx='lwh', alignment=ui.ALIGN_LEFT, name='directionSelect')
v.add_subview(direction)

#Voice toggle on UI
voice = ui.Switch(frame=(10,65,100,50))
v.add_subview(voice)
appex.set_widget_view(v)

#Ag
# switchSpeed =ui.Switch(frame=10,)

#Set default values for previous lane/speed values
lastSlowDown = ""
lastLane = ""
lastSpeed = 0
voice.value = 0

while True:
	
	#Write previous GPS before updating and sleeping.
	try:
		previousGPS = currentGPS
	except NameError:
		pass
	
	if platform.machine().startswith('iP'):
	
		#Turn on GPS and fetch current location
		location.start_updates()
		myLocation = location.get_location()
		location.stop_updates()
			
		#Update global GPS currentGPS for direction lookup	
		currentGPS = (myLocation['latitude'],myLocation['longitude'])
	
		#Values for finding station closest to current lat/lon
		v = {'lat': myLocation['latitude'], 'lon': myLocation['longitude']}
	
	else:					
		#Testing data for iPad
		#station 276
		v = {'lat': 44.97205, 'lon':  -93.38244}
	
	
		currentGPS = (44.97205,44.97205,-93.38244)
	
		#Station 266
		#v = {'lat': 44.97102, 'lon':  -93.49132}
	
	#Store closest location to current GPS
	myTP = getTravelPath()
	closestStation = closest(myTP, v)['station']
	
	#Load sensor data from MN website	
	latestSensorData = untangle.parse(str(getMNDOTData(), 'utf-8')).traffic_sample.sample
	
	#Count number of lanes displayed
	laneDisplayCount = 0
					
	#clean old values
	S1.text = ""
	S2.text = ""
	S3.text = ""
	
	#Loop on all stations to get best lane for each station
	for stationlist in getTravelPath():
	
		#Create array's that will store speed and lane data of relevant stations
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
					speeds.append(sensors['speed'])
					lane.append(k)
		
		#Confirm station has values
		if len(speeds)>0:
					
			#set max speed as int and clean unknow
			if max(speeds) == "UNKNOWN":
				maxSpeed = 65
				textSpeed = "Open"
			else:
				maxSpeed = int(max(speeds))
				textSpeed = maxSpeed
				
			#Tune lane switching speed used in voice update on S1
			if maxSpeed < 20:
				switchRate = 0
			elif maxSpeed < 40:
				switchRate = 2
			elif maxSpeed < 60:
				switchRate = 3
			else:
				switchRate = 40
			
			
			#Update Position 3 in UI for next station if first and second have been populated
			if laneDisplayCount > 1 and laneDisplayCount < 3:
				laneDisplayCount = laneDisplayCount + 1
				S3.text = "%s Lane: %s is at %s" % (stationlist['station'],lane[speeds.index(max(speeds))],textSpeed)
					
			#Update Position 2 in UI if position 1 has started
			if laneDisplayCount > 0 and laneDisplayCount < 2:
				laneDisplayCount = laneDisplayCount + 1
				S2.text = "%s Lane: %s is at %s" % (stationlist['station'],lane[speeds.index(max(speeds))],textSpeed)
				
				#Warn of upcomming slowddown and best future lane
				if ((lastSpeed / maxSpeed)  < .5) and lastSlowDown != stationDetails['station'] :
					voiceUpdate(lane,speeds,lastSlowDown,1)
					lastSlowDown = stationDetails['station']
					
			#Update position 1 in UI if current closest station matches current station
			if closestStation == stationlist['station']:
				laneDisplayCount = laneDisplayCount + 1			
				S1.text = "%s Lane: %s is at %s" % (stationlist['station'],lane[speeds.index(max(speeds))],textSpeed)
				
				#Update via Voice if switch is on and under the sleed limit
				if maxSpeed < 70 and (maxSpeed - lastSpeed) > switchRate:
					voiceUpdate(lane,speeds,lastLane,0)
					
					#Update last lane that was shared			
					lastLane = lane[speeds.index(max(speeds))]
			
					#update last speed for next check to avoid thrashing 
					lastSpeed = maxSpeed				

	#Sleep and check it all again
	time.sleep (15)