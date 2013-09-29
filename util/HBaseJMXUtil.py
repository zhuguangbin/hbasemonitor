'''
Created on 2013-9-27

@author: hadoop
'''
import re
import simplejson as json
import urllib2

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
        
    def parse(self, jmxInfo, metricGroupRegex, metricNameList=None):
        result = []
        
        p = re.compile(metricGroupRegex)
        groupList = jmxInfo['beans']
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

            
        
