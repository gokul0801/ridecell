from parking.models import Spot

def parseFile():
    f = file('coordinates.csv')
    for line in f:
        if '#' not in line:
            line = line.strip().replace(' ','')
            lat, long = line.split(',')
            spot = Spot(latitude=lat, longitude=long)
            spot.save()
    f.close()

parseFile()


        
