# -*- coding: utf-8 -*-
from django.forms import CharField,FileField,TextInput,Textarea,ModelForm,Select
from mongodbforms import DocumentForm,EmbeddedDocumentForm
from .models import *

class ClusterForm(DocumentForm):
    class Meta:
        document = Cluster
        embedded_field_name = 'cluster'
        fields = ['clusterId', 'masterJMXUrl','description', ]

