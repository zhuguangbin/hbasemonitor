# -*- coding: utf-8 -*-
import datetime
from django.db import models
from mongoengine import *

class Cluster(Document):
    clusterId = StringField(max_length=200,required=True,unique=True,help_text='cluster ID')
    masterJMXUrl = URLField(required=True,help_text='format: http://master:port/jmx')
    description = StringField(max_length=1000,help_text='description')
    zookeeperQuorum = StringField(max_length=1000,help_text='zookeeper quorum')
    masters = ListField()
    regionservers = ListField()


class HMasterStatistics(EmbeddedDocument):
    name = StringField(max_length=200,required=True,help_text='master server name')
    startTime = DateTimeField(help_text='hmaster start time')
    activeTime = DateTimeField(help_text='hmaster active time')
    isActiveMaster = BooleanField()
    coprocessors = ListField(help_text='hmaster coprocessors')

class RegionServerStatistics(EmbeddedDocument):
    name = StringField(max_length=200,required=True,help_text='regionserver name')
    statistics = DictField()

class ClusterStatistics(Document):
    clusterId = StringField(max_length=200,required=True,unique=True,primary_key=True,help_text='cluster id')
    masterStatistics = ListField(EmbeddedDocumentField(HMasterStatistics))
    rsStatistics = ListField(EmbeddedDocumentField(RegionServerStatistics))
    averageLoad = IntField()
    regionsInTransition = ListField()
    deadRegionServers = ListField()
    sampleTime = DateTimeField(default=datetime.datetime.now(),help_text='statistics sample time')
    
    meta = {
        'indexes': [
            'clusterId', ('clusterId', '-sampleTime')
        ]
    }    
