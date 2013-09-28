# -*- coding: utf-8 -*-
import datetime
from django.db import models
from mongoengine import *

class HMaster(EmbeddedDocument):
    ip = StringField(max_length=200,required=True,help_text='master ip')
    port = IntField(default=60000,help_text='master server port')
    infoPort = IntField(default=60010,help_text='master infoserver port')

class RegionServer(EmbeddedDocument):
    ip = StringField(max_length=200,required=True,help_text='regionserver ip')
    port = IntField(default=60020,help_text='regionserver port')
    infoPort = IntField(default=60030,help_text='regionserver infoserver port')

class Cluster(Document):
    clusterId = StringField(max_length=200,required=True,unique=True,help_text='cluster ID')
    masterJMXUrl = URLField(required=True,help_text='hmaster jmx url. example: http://master:port/jmx')
    masters = ListField(EmbeddedDocumentField(HMaster))
    regionservers = ListField(EmbeddedDocumentField(RegionServer))
    zookeeperQuorum = StringField(max_length=1000,help_text='zookeeper quorum')
    description = StringField(max_length=1000,help_text='description')

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
class Choice(EmbeddedDocument):
    choice_text = StringField(max_length=200)
    votes = IntField(default=0)

class Poll(Document):
    question = StringField(max_length=200)
    pub_date = DateTimeField(help_text='date published')
    choices = ListField(EmbeddedDocumentField(Choice))

    meta = {
        'indexes': [
            'question', 
            ('pub_date', '+question')
        ]
    }