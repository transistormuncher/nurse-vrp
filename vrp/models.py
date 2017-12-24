from django.db import models
from django.forms.models import ModelForm
from django.forms.widgets import *
from django.contrib.admin.widgets import AdminDateWidget
from django import forms
import subprocess
import os.path
import time
import pandas as pd
from django.db.models import Sum


# Create your models here.
class Address(models.Model):
	"""Model for addresses"""
	name = models.CharField(max_length= 100, blank=True, null=True)
	street = models.CharField(max_length= 100, blank=True, null=True)
	housenumber = models.CharField(max_length= 10, blank=True, null=True)
	postcode = models.IntegerField(blank=True, null=True)
	city = models.CharField(max_length= 50, blank=True, null=True)
	country = models.CharField(max_length= 20, blank=True, null=True, default= "Slovakia")
	latitude= models.DecimalField(max_digits=20, decimal_places=18, default=48.721287)
	longitude = models.DecimalField(max_digits=20, decimal_places=18, default= 18.5491726)

	def __str__(self):
		return u'[{}]_{}' .format(self.city, self.name)

	# necessary for create view
	@models.permalink
	def get_absolute_url(self):
		return ('address-detail', [self.id])

	# necessary to iterate over fields of object
	def get_fields(self):
		return [(field.name, field.value_to_string(self)) for field in Address._meta.fields]


class Vehicle(models.Model):
	"""Vehicle model"""
	name = models.CharField(max_length= 100)
	capacity = models.IntegerField(default=7, help_text="number of passenger seats")
	notes = models.TextField(null=True, blank= True)
	fuel_consumption = models.DecimalField(max_digits=4, decimal_places=2, default=8, help_text="Average fuel consumption per 100 km")

	def __str__(self):
		return u'{} ({} passenger seats)' .format(self.name, self.capacity)

	@models.permalink
	def get_absolute_url(self):
		return ('vehicle-detail', [self.id])

	def get_fields(self):
		return [(field.name, field.value_to_string(self)) for field in Vehicle._meta.fields]



class Route(models.Model):
	"""Route model:
	A route consist of
	- starting point
	- end point
	- stops in between start and end
	- vehicle
	
	A route is a subset of a tour. A tour states the VRP to be solved: all stops and all vehicles. 
	Solving the VRP creaates the routes, indicating which vehicle should service which stops in which order

	"""
	route_number = models.IntegerField()
	tour = models.ForeignKey("Tour", on_delete=models.CASCADE)
	vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
	# stops = needs to be an array field containign all stops in the correct order
	distance = models.DecimalField(max_digits=7, decimal_places=2)
	duration = models.DecimalField(max_digits=7, decimal_places=2)
	point_list = models.TextField(null=True, blank= True)
	instructions = models.TextField(null=True, blank= True)

	def __str__(self):
		return u'Route {}_{} ' .format(self.tour.id, self.route_number)

	@models.permalink
	def get_absolute_url(self):
		return ('route-detail', [self.id])

	def get_fields(self):
		return [(field.name, field.value_to_string(self)) for field in Route._meta.fields]

	def get_total_distance(self):
		dist = 0
		for s in  self.stop_set.all():
			dist += s.distance
			self.distance = dist
		return(dist)


	def get_total_duration(self):
		duration = 0
		for s in  self.stop_set.all():
			duration += s.duration
			self.duration = duration
		return(duration)





class Stop(models.Model):
	address = models.ForeignKey(Address, on_delete=models.CASCADE)
	route = models.ForeignKey('Route',  on_delete=models.CASCADE)
	sequence = models.IntegerField()
	distance = models.DecimalField(max_digits=7, decimal_places=2, default=0)
	duration = models.DecimalField(max_digits=7, decimal_places=2, default=0)

	class Meta:
		unique_together = (('route', 'sequence'), )
		ordering = ['route', 'sequence']

	def __str__(self):
		return u'{} [Stop {}] ' .format(self.route, self.sequence)




from .model_functions import create_routes
class Tour(models.Model):
	"""Tour model:
	A tour consist of
	- starting point
	- end point
	- stops in between start and end
	- vehicles

	"""
	date = models.DateField()
	stops = models.ManyToManyField(Address)
	start_location = models.ForeignKey(Address, related_name='tour_start', on_delete=models.CASCADE)
	end_location = models.ForeignKey(Address, related_name='tour_end', on_delete=models.CASCADE)
	vehicles = models.ManyToManyField(Vehicle)
	drivers = models.IntegerField(default=3)
	notes = models.TextField(null=True, blank= True)

	def __str__(self):
		return u'Tour of {}' .format(self.date)

	@models.permalink
	def get_absolute_url(self):
		return ('tour-detail', [self.id])

	def get_fields(self):
		return [(field.name, field.value_to_string(self)) for field in Tour._meta.fields]

	def solve_vrp(self):
		data_dir = "data/"
		fname = "data/dist_mat_[tour_{}].csv".format(self.id)
		while not os.path.isfile(fname):
			time.sleep(1)
			print("waiting for input files to be created")
		p = subprocess.Popen(['java', '-jar', 'java/vrp_solver.jar', str(self.id), data_dir])
		return("solved VRP")

	def parse_xml(self):
		fname = "data/vrp_output/solution_tour[{}].xml".format(self.id)
		while not os.path.isfile(fname):
			time.sleep(1)
			print("waiting for xml file to be created")
		create_routes(self);
		return("created routes")






# should be in forms. py


class TourForm(ModelForm):
	"""Customized form for the tour model to have nicer widgets"""

	class Meta:
		model = Tour
		fields = ["date", "start_location", "end_location", "stops", "vehicles", "drivers", "notes"]

	def __init__(self, *args, **kwargs):

		super(TourForm, self).__init__(*args, **kwargs)

		self.fields["date"].widget = AdminDateWidget() #DateInput()
		self.fields["start_location"].widget = Select()
		self.fields["start_location"].queryset = Address.objects.all()
		self.fields["end_location"].widget = Select()
		self.fields["end_location"].queryset = Address.objects.all()
		self.fields["stops"].widget = CheckboxSelectMultiple()
		self.fields["stops"].queryset = Address.objects.all()
		self.fields["vehicles"].widget = CheckboxSelectMultiple()
		self.fields["vehicles"].queryset = Vehicle.objects.all()
		self.fields["drivers"].widget = NumberInput()
		self.fields["notes"].widget = Textarea()

















