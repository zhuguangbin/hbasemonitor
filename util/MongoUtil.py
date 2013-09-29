'''
Created on 2013-9-27

@author: hadoop
'''
import pymongo
from pymongo import MongoClient

class Mongo(object):
    '''
    classdocs
    '''


    def __init__(self,host,port,dbName):
        '''
        Constructor
        '''
        self.client = MongoClient(host,port)
        self.db = self.client[dbName]
        
    def save(self,jmxdata):
        
        collection = self.db[collectionName]
        collection.insert(data)
        