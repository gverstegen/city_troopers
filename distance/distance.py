#!/usr/bin/jython
from org.opentripplanner.scripting.api import OtpsEntryPoint


# Instantiate an OtpsEntryPoint
otp = OtpsEntryPoint.fromArgs(['--graphs', '.',
                               '--router', 'sto'])

# Start timing the code
import time
start_time = time.time()

# Get the default router
router = otp.getRouter('sto')


# Read Points of Destination - The file points.csv contains the columns GEOID, X and Y.
points = otp.loadCSVPopulation('centroids_sto.csv', 'Y', 'X')
dests = otp.loadCSVPopulation('centroids_sto.csv', 'Y', 'X')


for h in range(7, 19):
  for m in range(0,60,30):

    # Create a default request for a given time
    req = otp.createRequest()
    req.setDateTime(2015, 12, 28, h, m, 00)
    req.setMaxTimeSec(3600) # 1h = 3600 seconds , 2h = 7200 seconds
    req.setModes('WALK,TRANSIT,BUS,TRAM,RAIL,SUBWAY')  # ("TRAM,RAIL,SUBWAY,FUNICULAR,GONDOLA,CABLE_CAR,BUS")


    # Create a CSV output
    matrixCsv = otp.createCSVOutput()
    matrixCsv.setHeader([ 'mode', 'depart_time', 'origin', 'destination', 'walk_distance', 'travel_time' ]) # travel_time in seconds

    # Start Loop
    for origin in points:
      print "Processing origin: ", str(h)+"-"+str(m)," ", origin.getStringData('idhex')
      req.setOrigin(origin)
      spt = router.plan(req)
      if spt is None: continue

      # Evaluate the SPT for all points
      result = spt.eval(dests)

      # Add a new row of result in the CSV output
      for r in result:
        matrixCsv.addRow([ 'public transport', str(h) + ":" + str(m) + ":00", origin.getStringData('idhex'), r.getIndividual().getStringData('idhex'), r.getWalkDistance() , r.getTime()])

    # Save the result
    matrixCsv.save('traveltime_matrix_sto_pt_'+ str(h)+"-"+str(m) + '.csv')


# Stop timing the code
print("Elapsed time was %g seconds" % (time.time() - start_time))
