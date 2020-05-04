

def fill_gaps(list):
    # Find first altitude
    first_altitude = 0
    for item in list:
        if item != -10000:
            first_altitude = item
            break
    for i in range(len(list)):
        if list[i] == -10000:
            list[i] = first_altitude
        else:
            first_altitude = list[i]
    return list

def trackpoint_to_dic(trackpoint):
    from dateutil.parser import parse
    import time
    dic = {}
    power_available = False
    if len(trackpoint.getElementsByTagName('Time')) > 0:
        dic["TimeStamp"] = time.mktime(parse(trackpoint.getElementsByTagName('Time')[0].firstChild.data).timetuple())
    if len(trackpoint.getElementsByTagName('HeartRateBpm')) > 0:
        dic["HeartRate"] = int(trackpoint.getElementsByTagName('HeartRateBpm')[0].childNodes[1].firstChild.data)
    if len(trackpoint.getElementsByTagName('DistanceMeters')) > 0:
        dic["DistanceMeters"] = float(trackpoint.getElementsByTagName('DistanceMeters')[0].firstChild.data)
    if len(trackpoint.getElementsByTagName('ns3:Speed')) > 0:
        dic["Speed"] = 3.6*float(trackpoint.getElementsByTagName('ns3:Speed')[0].firstChild.data)
    if len(trackpoint.getElementsByTagName('ns3:Watts')) > 0:
        dic["Power"] = int(trackpoint.getElementsByTagName('ns3:Watts')[0].firstChild.data)
        power_available = True
    if len(trackpoint.getElementsByTagName('Cadence')) > 0:
        dic["Cadence"] = int(trackpoint.getElementsByTagName('Cadence')[0].firstChild.data)
    if len(trackpoint.getElementsByTagName('AltitudeMeters')) > 0:
        dic["Altitude"] = float(trackpoint.getElementsByTagName('AltitudeMeters')[0].firstChild.data)
    if len(trackpoint.getElementsByTagName('LatitudeDegrees')) > 0:
        dic["Latitude"] = float(trackpoint.getElementsByTagName('LatitudeDegrees')[0].firstChild.data)
    if len(trackpoint.getElementsByTagName('LongitudeDegrees')) > 0:
        dic["Longitude"] = float(trackpoint.getElementsByTagName('LongitudeDegrees')[0].firstChild.data)
    return (dic, power_available)

def plot_activity(filename):
    from xml.dom import minidom
    mydoc = minidom.parse(filename)
    trackpoints = mydoc.getElementsByTagName('Trackpoint')

    time = []
    distance = []
    altitude = []
    latitude = []
    longitude = []

    for trackpoint in trackpoints:
        parsed, power_available = trackpoint_to_dic(trackpoint)
        time.append(parsed["TimeStamp"])

        if "DistanceMeters" in parsed:
            distance.append(parsed["DistanceMeters"])
        else:
            distance.append(0)

        if "Altitude" in parsed:
            altitude.append(parsed["Altitude"])
        else:
            altitude.append(-10000)

        if "Latitude" in parsed:
            latitude.append(parsed["Latitude"])
        else:
            latitude.append(-10000)

        if "Longitude" in parsed:
            longitude.append(parsed["Longitude"])
        else:
            longitude.append(-10000)
    
    altitude = fill_gaps(altitude)
    latitude = fill_gaps(latitude)
    longitude = fill_gaps(longitude)

    import math

    x = []
    y = []
    z = []
    R = 6352.8 # Earth radix
    for i in range(len(altitude)):
        x.append(R * math.cos(math.radians(latitude[i])) * math.cos(math.radians(longitude[i])))
        y.append(R * math.cos(math.radians(latitude[i])) * math.sin(math.radians(longitude[i])))
        z.append(R * math.sin(math.radians(latitude[i])) + altitude[i])
    
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(x, y, z)
    plt.show()

plot_activity("short_ride.tcx")