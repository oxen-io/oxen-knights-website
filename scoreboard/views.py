from __future__ import unicode_literals
from django.views.generic import TemplateView
from django.shortcuts import render , redirect
from scoreboard.forms import HomeForm
from csv import reader
import string
import json
import re
# Create your views here.

class RankingReward(TemplateView):
    template_name = 'templatesviews/rankingreward.html'
    def get(self, request, *args, **kwargs):
        form = HomeForm()
        return render(request,self.template_name, {'form':form})

class PointSystem(TemplateView):
    template_name = 'point-system.html'
    def get(self, request, *args, **kwargs):
        form = HomeForm()
        return render(request,self.template_name, {'form':form})

def home(request):
    return render(request,'index.html')
