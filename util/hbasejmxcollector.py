
import datetime,time

from HBaseJMXUtil import *
import pymongo
from pymongo import MongoClient

fetcher = JMXFetcher()
parser = JMXParser()

def getCluster(masterjmxdata):
    result = parser.parse(masterjmxdata, 'hadoop:service=Master,name=Master$',['ClusterId','ServerName','RegionServers','ZookeeperQuorum'])
    
    cluster = {}
    cluster['clusterId']=result[0]['ClusterId']
    cluster['masterJMXUrl']=masterJMXUrl
    cluster['zookeeperQuorum']=result[0]['ZookeeperQuorum']
    cluster['masters']=[(result[0]['ServerName'])]
    cluster['regionservers']=[rs['key'] for rs in result[0]['RegionServers']]
    
    return cluster
    
def saveJMX(db,jmxdata,filter=None):
    jmxbeans = jmxdata['beans']
    for jmxbean in jmxbeans:
        cleanedjmxbean = dict((k.replace('.',','),v) for k,v in jmxbean.iteritems())
        cleanedjmxbean['sampleTime'] = str(datetime.datetime.now())
        try:
            jmxname = cleanedjmxbean['name']
            if filter is not None:
                if jmxname in filter:
                    collection = jmxname
                    db[collection].insert(cleanedjmxbean)
            else :
                collection = jmxname
                db[collection].insert(cleanedjmxbean)
        except Exception,e:
            print e
    

if __name__ == '__main__':
    
#     clusters = [{'masterJMXUrl':'http://10.2.6.152:60010/jmx', 'clustername':'hbase0' }, {'masterJMXUrl':'http://10.1.6.10:60010/jmx', 'clustername':'hbase1' }, {'masterJMXUrl':'http://10.1.6.59:60010/jmx', 'clustername':'hbase2' }]
    clusters = [{'masterJMXUrl': 'http://10.1.77.87:60010/jmx', 'clustername': 'hbaseqa'}]
    client = MongoClient()
              
    while True :
        
        for cluster in clusters:
            
            masterJMXUrl = cluster['masterJMXUrl']
            clustername = cluster['clustername']
    
            db = client[clustername]
            
            masterjmxdata = fetcher.getJMX(masterJMXUrl)
            clusterdesc = getCluster(masterjmxdata)
            masterip = clusterdesc['masters'][0].split(',')[0]
            saveJMX(db, masterjmxdata,filter=["hadoop:service=Master,name=Master","hadoop:service=Master,name=MasterStatistics","hadoop:service=HBase,name=RPCStatistics-60000"])
            
            for rs in clusterdesc['regionservers']:
                rsip = rs.split(',')[0]
                rsJMXUrl ='http://'+ rsip + ':60030/jmx'
                rsjmxdata = fetcher.getJMX(rsJMXUrl)
                saveJMX(db, rsjmxdata,filter=["hadoop:service=RegionServer,name=RegionServer","hadoop:service=RegionServer,name=RegionServerDynamicStatistics","hadoop:service=HBase,name=RPCStatistics-60020"])
            
        
        time.sleep(1)