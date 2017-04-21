from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
from models import Spot
import json
from math import radians, cos, sin, asin, sqrt, atan2
from django.utils import timezone

def index(request):
    req_lat = float(request.GET['lat'])
    req_long = float(request.GET['long'])
    req_radius = float(request.GET['radius'])    

    checkReservationsComplete()
    spotsHash = getAvailableSpots(req_lat, req_long, req_radius)
    result = []
    if spotsHash != {}:
        # Display spots in sorted order by distance to user location
        arr = sorted(spotsHash.iteritems(), key = lambda x:x[1])
        for x in arr:
            spot = Spot.objects.get(id=x[0])
            spotObj = {'id': spot.id,
                       'lat': spot.latitude,
                       'long': spot.longitude,
                      }
            result.append(spotObj)  
        return HttpResponse(json.dumps(result, indent=4), content_type="application/json")
    else:
        return HttpResponse("No available spots in that radius from user location")


def checkReservationsComplete():
    # Check if any reserved spots are past their allocated time frame
    # we make the assumption car will have been moved after completion of reserved time
    # and that space can be marked as available

    currTime = timezone.now()
    for spot in Spot.objects.filter(available=False):
        if (currTime - spot.parkingStartTime).seconds > spot.parkingAllocatedTime*60:
            spot.available = True
            spot.parkingStartTime = None
            spot.parkingAllocatedTime = None
            spot.save()


def getAvailableSpots(req_lat, req_long, req_radius):
    # Traverse through available spots within the radius requested by user
    # Store distances in hash
    hash = {}
    for spot in Spot.objects.filter(available=True):
        dist = getDistance(req_lat, req_long, spot.latitude, spot.longitude)
        if dist <= req_radius:
            hash[spot.id] = dist
    return hash
 

def reserve(request):
    req_spot_id = request.GET['parking_spot']
    req_time = float(request.GET['time_range'])
    
    checkReservationsComplete()
    spot = Spot.objects.get(id=req_spot_id)
    if spot.available:
        spot.available = False
        spot.parkingStartTime = timezone.now()
        spot.parkingAllocatedTime = req_time
        spot.save()
        result = {'id': spot.id, 
	          'lat': spot.latitude,
                  'long': spot.longitude,
	          'startTime': spot.parkingStartTime.strftime('%H:%M'),
                  'reservedTime': '%s mins' % req_time
                 }
        return HttpResponse(json.dumps(result, indent=4), content_type="application/json")
    else:
        return HttpResponse("That spot has already been taken. Try reserving another spot")
	      
    
# Get distance in miles between two coordinates
def getDistance(lat1, long1, lat2, long2):
    lat1, long1, lat2, long2 = map(radians, [lat1, long1, lat2, long2])
    dlon = long2 - long1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    R = 6373.0
    distance = R * c * .621371
    return distance


    
    
