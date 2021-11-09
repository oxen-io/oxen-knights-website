from __future__ import unicode_literals
from django.views.generic import TemplateView
from django.shortcuts import render , redirect
from scoreboard.forms import HomeForm
from csv import reader
import string
import json
import re
import pandas as pd
import os
# Create your views here.
filepath = os.path.abspath(os.getcwd()) + '/'
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

	def post(self,request):
		form = HomeForm(request.POST)

		if form.is_valid():
			handle = form.cleaned_data['text']
			if handle:
				if handle[0] == '@':
					handle = handle[1:].lower()
				else:
					handle = handle.lower()
				if 'check' in request.POST:
					result = handle

			form = HomeForm()
			#return redirect ('home:home')
		with open(filepath + 'scoreboard.json', 'r') as F:
			json_file = json.loads(F.read())
		json_file =  {k.lower(): v for k, v in json_file.items()}
		print(json_file)
		if handle in json_file:
			current_points = json_file[handle]['points']

			df = pd.read_csv(filepath + 'ranking.csv')
			rankings = df['RANK'].tolist()
			index = rankings.index(json_file[handle]['ranking'])
			next_level_points = df['POINTS'].tolist()[index+1]
			this_level_points = df['POINTS'].tolist()[index]
			points_needed = next_level_points - current_points
			points_between_levels = next_level_points - this_level_points
			points_this_level = current_points - this_level_points
			percent_finished = int(round(points_this_level / points_between_levels,2) * 100)
			current_rank = rankings[index]
			next_rank = rankings[index+1]
			status = 1
		else:
			current_points = 0
			percent_finished = 0
			points_needed = 0
			current_rank = 0
			next_rank =0
			status =0


		args = {'form': form, 'handle':handle, 'points':current_points,'percent':percent_finished,'needed':points_needed,'current_rank':current_rank,'next_rank':next_rank,'status':status}
		return render(request, self.template_name, args )

#def home(request):
#	return render(request,'index.html')


class home(TemplateView):
	template_name = 'home.html'
	def get(self, request, *args, **kwargs):
		form = HomeForm()
		with open(filepath + 'toptweet.json', 'r') as F:
			toptweet = json.loads(F.read())
		with open(filepath + 'scoreboard.json', 'r') as F:
			json_file = json.loads(F.read())
		top_knight = list(json_file.keys())[0]
		top_knight_values = list(json_file.values())[0]
		args = {'form':form,'top_tweet':toptweet,'scoreboard':json_file,'top_knight':top_knight,'top_knight_values':top_knight_values}

		return render(request, self.template_name, args )

	def post(self,request):
		form = HomeForm(request.POST)

		if form.is_valid():
			handle = form.cleaned_data['text']
			if handle:
				if handle[0] == '@':
					handle = handle[1:].lower()
				else:
					handle = handle.lower()
				if 'check' in request.POST:
					result = handle

			form = HomeForm()
			#return redirect ('home:home')
		with open(filepath +  'scoreboard.json', 'r') as F:
			json_file = json.loads(F.read())
		json_file =  {k.lower(): v for k, v in json_file.items()}
		top_knight = list(json_file.keys())[0]
		top_knight_values = list(json_file.values())[0]
		if handle in json_file:
			current_points = json_file[handle]['points']
			tweets = json_file[handle]['tweets']
			likes = json_file[handle]['likes']
			retweets = json_file[handle]['retweets']
			ranking = json_file[handle]['ranking']
			df = pd.read_csv(filepath + 'ranking.csv')
			rankings = df['RANK'].tolist()
			index = rankings.index(json_file[handle]['ranking'])
			next_level_points = df['POINTS'].tolist()[index+1]
			this_level_points = df['POINTS'].tolist()[index]
			points_needed = next_level_points - current_points
			points_between_levels = next_level_points - this_level_points
			points_this_level = current_points - this_level_points
			percent_finished = int(round(points_this_level / points_between_levels,2) * 100)
			current_rank = rankings[index]
			next_rank = rankings[index+1]
			status = 1
		else:
			current_points = 0
			tweets = 0
			likes = 0
			retweets = 0
			ranking = 0
			percent_finished = 0
			points_needed = 0
			current_rank = 0
			next_rank = 0
			status = 0
		with open(filepath + 'toptweet.json', 'r') as F:
			toptweet = json.loads(F.read())
		with open(filepath + 'scoreboard.json', 'r') as F:
			json_file = json.loads(F.read())
		top_knight = list(json_file.keys())[0]
		top_knight_values = list(json_file.values())[0]

		args = {'anchor':'scoreboard','ranking':ranking,'tweets':tweets,'likes':likes,'retweets':retweets,'form': form,'top_tweet':toptweet,'top_knight':top_knight,'scoreboard':json_file,'top_knight_values':top_knight_values, 'handle':handle, 'points':current_points,'percent':percent_finished,'needed':points_needed,'current_rank':current_rank,'next_rank':next_rank,'status':status}
		return render(request, self.template_name, args )
