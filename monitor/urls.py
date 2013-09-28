from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
from settings import HERE

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'monitor.core.views.index',),
    url(r'^resources/(?P<path>.*)$', 'django.views.static.serve',{'document_root': HERE+'/htdocs/resources/'}),
    url(r'^menu/getAccordionItem$', 'monitor.core.views.getAccordionItem'),
    url(r'^menu/getAllTreeNode/(?P<parentId>.*)$', 'monitor.core.views.getAllTreeNode'),
    url(r'^overview$','monitor.core.views.overview'),
    url(r'^cluster$','monitor.core.views.cluster'),
    url(r'^cluster/(?P<action>.*)$','monitor.core.views.clusterAction'),

    # Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
