import csv
import numpy
import zerorpc
import os

from subprocess import call

from nearpy import Engine
from nearpy.hashes import RandomBinaryProjections

from redis import Redis
from nearpy.storage import RedisStorage


# Dimension of our vector space
dimension = 68

# Create a random binary hash with 10 bits
rbp = RandomBinaryProjections('rbp', 10)

# Create engine with pipeline configuration
redis_storage = RedisStorage(Redis(host='localhost', port=6379, db=0))
engine = Engine(dimension, lshashes=[rbp], storage=redis_storage)

index = 0
with open("Adele.csv", "rb") as csvfile:
    featurereader = csv.reader(csvfile, delimiter=',')
    for row in featurereader:
        index = index+1
        x = numpy.array(row, dtype='|S4')
        y = x.astype(numpy.float)
        engine.store_vector(y, 'Adele - Hello_%d' % index)

index=0        
with open("BlurredLines.csv", "rb") as csvfile:
    featurereader = csv.reader(csvfile, delimiter=',')
    for row in featurereader:
        index = index+1
        x = numpy.array(row, dtype='|S4')
        y = x.astype(numpy.float)
        engine.store_vector(y, 'Robin Thicke - Blurred Lines ft. T.I. Pharrell_%d' % index)

index=0        
with open("CallMeMaybe.csv", "rb") as csvfile:
    featurereader = csv.reader(csvfile, delimiter=',')
    for row in featurereader:
        index = index+1
        x = numpy.array(row, dtype='|S4')
        y = x.astype(numpy.float)
        engine.store_vector(y, 'Carly Rae Jepsen - Call Me Maybe_%d' % index)

index=0        
with open("Happy.csv", "rb") as csvfile:
    featurereader = csv.reader(csvfile, delimiter=',')
    for row in featurereader:
        index = index+1
        x = numpy.array(row, dtype='|S4')
        y = x.astype(numpy.float)
        engine.store_vector(y, 'Pharrell Williams - Happy_%d' % index)
        
index=0        
with open("OneMoreNight.csv", "rb") as csvfile:
    featurereader = csv.reader(csvfile, delimiter=',')
    for row in featurereader:
        index = index+1
        x = numpy.array(row, dtype='|S4')
        y = x.astype(numpy.float)
        engine.store_vector(y, 'Maroon 5 - One More Night_%d' % index)
        
index=0        
with open("Royals.csv", "rb") as csvfile:
    featurereader = csv.reader(csvfile, delimiter=',')
    for row in featurereader:
        index = index+1
        x = numpy.array(row, dtype='|S4')
        y = x.astype(numpy.float)
        engine.store_vector(y, 'LORDE - Royals_%d' % index)
        
index=0        
with open("SeeYouAgain.csv", "rb") as csvfile:
    featurereader = csv.reader(csvfile, delimiter=',')
    for row in featurereader:
        index = index+1
        x = numpy.array(row, dtype='|S4')
        y = x.astype(numpy.float)
        engine.store_vector(y, 'Wiz Khalifa - See You Again ft. Charlie Puth_%d' % index)
        
index=0        
with open("TiKToK.csv", "rb") as csvfile:
    featurereader = csv.reader(csvfile, delimiter=',')
    for row in featurereader:
        index = index+1
        x = numpy.array(row, dtype='|S4')
        y = x.astype(numpy.float)
        engine.store_vector(y, 'Ke$ha - TiK ToK_%d' % index)
        
index=0        
with open("UptownFunk.csv", "rb") as csvfile:
    featurereader = csv.reader(csvfile, delimiter=',')
    for row in featurereader:
        index = index+1
        x = numpy.array(row, dtype='|S4')
        y = x.astype(numpy.float)
        engine.store_vector(y, 'Mark Ronson - Uptown Funk ft. Bruno Mars_%d' % index)
        
index=0        
with open("WeFoundLove.csv", "rb") as csvfile:
    featurereader = csv.reader(csvfile, delimiter=',')
    for row in featurereader:
        index = index+1
        x = numpy.array(row, dtype='|S4')
        y = x.astype(numpy.float)
        engine.store_vector(y, 'Rihanna - We Found Love ft. Calvin Harris_%d' % index)

print "END"

class kNN(object):
    def __init__(self, engine):
        self.engine = engine
        
    def startNNS(self, name):
        os.system("python /Users/pascal/Research/libraries/pyAudioAnalysis/audioAnalysis.py featureExtractionFile -i ../server/tmp/test.wav -mw 1.0 -ms 1.0 -o ../server/tmp/output")
        index=0
        results={}
        current_highest = ""
        with open("../server/tmp/output.csv", "rb") as csvfile:
            featurereader = csv.reader(csvfile, delimiter=',')
            for row in featurereader:
                index = index+1
                x = numpy.array(row, dtype='|S4')
                y = x.astype(numpy.float)
                print y
                current = self.engine.neighbours(y)
                print current
                result = current[0][1].partition("_")[0]
                if result in results:
                    results[result] = results[result]+1
                else:
                    results[result] = 1
            
            highest=0      
            for key in results.keys():
                if highest < results[key]:
                    highest = results[key]
                    current_highest = key    
        
        return str(current_highest)

s = zerorpc.Server(kNN(engine))
s.bind("tcp://0.0.0.0:4242")
s.run()
