# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django import forms
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.utils import simplejson

import xml.dom.minidom  
import datetime

import mongoengine
from mongoengine import QuerySet

from monitor.settings import HERE
from .models import *
from .forms import *

def index(request):
    return render_to_response('index.html')

def getAccordionItem(request):
    doc = xml.dom.minidom.parse(HERE+'/core/modules.xml')  
    data=[dict(node.attributes.items()) for node in doc.getElementsByTagName("sub_system")]
    return HttpResponse(simplejson.dumps(data))

def getAllTreeNode(request,parentId):
    doc = xml.dom.minidom.parse(HERE+'/core/modules.xml')  
    node = doc.getElementById(parentId)
    data=[dict(zip(['pid','id','text','iconCls','attributes'], [m.parentNode.getAttribute('id'),m.getAttribute('id'), \
         m.getAttribute('text'),m.getAttribute('iconCls'),{'url':m.getAttribute('url')}])) \
         for m in node.getElementsByTagName("module")]
    return HttpResponse(simplejson.dumps(data))

def overview(request):
    return render_to_response('overview.html')
        
def cluster(request):
    return render_to_response('cluster.html')
def clusterAction(request,action):
    if action=='find':
        data = Cluster.objects.to_json()
        print 'cluster results: '+ data
        return HttpResponse(data)
    if action=='add':
        form = ClusterForm(request.POST or None)
        url = '/cluster/add'
        if request.method == "POST":
            if form.is_valid():
                o=form.save()
                data={'success':True,'msg':"成功增加一个集群配置。",'obj':'','isAdd':True}
                print data
                return HttpResponse(simplejson.dumps(data))
        t = get_template('cluster_pop.html')
        c = RequestContext(request,locals())
        return HttpResponse(t.render(c))
    if action=='del':
        ids=request.GET['ids']
        for id in ids.split(","):
            Cluster.objects(clusterId=id).delete()
        data={'success':True,'msg':"成功删除一个集群配置。",'obj':None}
        return HttpResponse(simplejson.dumps(data))
    if action.startswith('edit')>0: 
        id=action.split("/")[-1]
        instance = Cluster.objects.get(clusterId=id)
        print instance
        form = ClusterForm(request.POST or None, instance = instance) 
        url = '/cluster/edit/'+id
        if request.method == "POST":
            if form.is_valid():
                o=form.save()
                data={'success':True,'msg':"成功修改一个集群配置。",'obj':'','isAdd':False}
                return HttpResponse(simplejson.dumps(data))
        t = get_template('cluster_pop.html')
        c = RequestContext(request,locals())
        return HttpResponse(t.render(c))       

