import numpy
import os
import csv
import web

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
db = web.database(dbn='sqlite', db='sorch.db')

def insertVector(id, vector):
     engine.store_vector(vector, id)
     
def getNN(vector):
    return engine.neighbours(vector)
    
def insertMetadata(id, url, artist, title, length):
    db.insert(id=id, url=url, artist=artist, title=title, length=length)
    
def getMetadataById(id):
    try:
        return db.select('songs', where='id=$id', vars=locals())[0]
    except IndexError:
        return None