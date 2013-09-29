'''
Created on 2013-9-27

@author: hadoop
'''
import re
import simplejson as json
import urllib2
from .models import *

class JMXFetcher(object):
        
    def getJMX(self, url):
        try:
            request = urllib2.Request(url)
            request.add_header('Content-Type', 'application/json')
            response = urllib2.urlopen(request)
            if response.code == 200 :
                data = response.read()
            return json.loads(data.strip())
        except urllib2.HTTPError, e:
            print e
        
class JMXParser(object):
        
    def parse(self, jmxJson, metricGroupRegex, metricNameList=None):
        result = []
        
        p = re.compile(metricGroupRegex)
        groupList = jmxJson['beans']
        for item in groupList:
            groupName = item['name']
            if (p.match(groupName)):
                if metricNameList == None or len(metricNameList) == 0:
                    result.append(item)
                else:
                    aGroup = {}
                    for metric in metricNameList:
                        try:
                            name = metric
                            value = item[metric]
                            aGroup[name] = value
                        except Exception, e:
                            print 'error while parsing hbase metrics: %s , %s ' %(metric, e)
                            raise e
                    result.append(aGroup)
            
        return result

fetcher = JMXFetcher()
parser = JMXParser()
    
def getCluster(masterJMXUrl,description):
    jmxdata = fetcher.getJMX(masterJMXUrl)
    if jmxdata:
        result = parser.parse(jmxdata, 'hadoop:service=Master,name=Master$',['ClusterId','ServerName','RegionServers','ZookeeperQuorum'])
        clusterId=result[0]['ClusterId']
        zookeeperQuorum=result[0]['ZookeeperQuorum']
        masters=[(result[0]['ServerName'])]
        regionservers = [rs['key'] for rs in result[0]['RegionServers']]
        cluster = Cluster()
        cluster.clusterId=clusterId
        cluster.masterJMXUrl=masterJMXUrl
        cluster.description=description
        cluster.zookeeperQuorum=zookeeperQuorum
        cluster.masters=masters
        cluster.regionservers=regionservers
        return cluster
        
        
            
        
