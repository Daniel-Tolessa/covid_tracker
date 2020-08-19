from django.shortcuts import render
import requests 
from datetime import datetime
import pandas as pd
import pygal

# Create your views here.
today = datetime.today()

today_string = today.strftime("%Y-%m-%d")

url_history = "https://covid-193.p.rapidapi.com/history?country=all"

history_dict = {
			'x-rapidapi-key': "f855f3e5c2mshc773b5eadcc276fp1fb183jsnda1e378419d2" #encrypt the api key
		 }
		 
history_record = requests.request("GET", url_history, headers=history_dict)

history = history_record.json() 

countries = history["response"]

def home_page(request):

	#print (history["response"][0]["deaths"]["total"])

	context = {
        "total_deaths": "{:,}".format(history["response"][0]["deaths"]["total"]),
        "new_death" : history["response"][0]["deaths"]["new"],
        "total_cases": "{:,}".format(history["response"][0]["cases"]["total"]),
        "new_cases" : history["response"][0]["cases"]["new"],
        "total_recovered": "{:,}".format(history["response"][0]["cases"]["recovered"]), 
        "active_case" : "{:,}".format(history["response"][0]["cases"]["active"]),
        "critical_case" : "{:,}".format(history["response"][0]["cases"]["critical"]),
        "last_updated" : today.strftime("%b %d %I:%M %p"),
    }

	return render(request , 'index.html', context)

def about_country(request):
	# print (request.GET)
	# print (request.POST)
	user_input = request.POST.get('title')
	print (user_input)
	country_list = "https://covid-193.p.rapidapi.com/countries" 

	country_dict = {
				'x-rapidapi-key': "f855f3e5c2mshc773b5eadcc276fp1fb183jsnda1e378419d2" #encrypt the api key
			 }
			 
	country_record = requests.request("GET", country_list, headers=country_dict)

	all_countries = country_record.json() 

	countries = all_countries["response"]
	url_history = "https://covid-193.p.rapidapi.com/history?country=all"
	if user_input is None:
		url_history = url_history.replace("all"  , "USA")
	else:
		url_history = url_history.replace("all"  , user_input)
	history_dict = {
				'x-rapidapi-key': "f855f3e5c2mshc773b5eadcc276fp1fb183jsnda1e378419d2" #encrypt the api key
			 }
	history_record = requests.request("GET", url_history, headers=history_dict)
	history = history_record.json()
	country_records = history["response"]
	context = {}  
	for country_record in country_records:
		if country_record["country"] == user_input:
			context["countries"] = countries
			context["country"] =  user_input
			context["total_deaths"] = "{:,}".format(country_record["deaths"]["total"])
			context["total_cases"] = "{:,}".format(country_record["cases"]["total"])
			context["recovered"] = "{:,}".format(country_record["cases"]["recovered"])
			context["active_case"] = "{:,}".format(country_record["cases"]["active"])
			context["critical_case"] = "{:,}".format(country_record["cases"]["critical"])
			context["new_cases"] = country_record["cases"]["new"] 
			context["new_deaths"] = country_record["deaths"]["new"]
			break
		else:
			context["country"] = ""
			context["countries"] = countries


	# context = {}
	# for country in countries:
	# 	if user_input == country:
	# 		context["input"] = ""
	# 		context["user_input"] = user_input
	# 		context["countries"] = countries
	# 		context["total_deaths"] = "{:,}".format(country["deaths"]["total"])
	# 		context["total_cases"] = "{:,}".format(country["cases"]["total"])
	# 		context["recovered"] = "{:,}".format(country["cases"]["recovered"])
	# 		context["active_case"] = "{:,}".format(country["cases"]["active"])
	# 		context["critical_case"] = "{:,}".format(country["cases"]["critical"])
	# 		context["new_cases"] = country["cases"]["new"]
	# 	else:
	# 		context["input"] = "Sorry , the country isn't found "

	return render(request , 'allcountry.html', context)

def about_page(request):
	return render(request , 'about.html' , {})
def covidcase_graph(request):
	bar_chart = pygal.Bar()
	bar_chart.title = "Covid cases record globally"
	bar_chart.add("F" , [1 , 2, 4, 5])
	bar_chart.render_to_file("static/img/abc.svg")
	context = {"aaa" : bar_chart}
	return (request , 'index.html' , context)

###
def covideath_graph(request):
	bar_chart = pygal.Bar()
	bar_chart.title = "Covid cases world wide"
	bar_chart.add("F" , [11 , 21 , 55, 12])
	bar_chart.render_to_file("static/img/rer.svg")
	context["graph"] = bar_chart
	return (request , 'index.html' , context)
