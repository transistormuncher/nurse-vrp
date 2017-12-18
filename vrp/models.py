from django.db import models
from django.forms.models import ModelForm
from django.forms.widgets import *
from django.contrib.admin.widgets import AdminDateWidget
from django import forms

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
	start_location = models.ForeignKey(Address, related_name='start_address', on_delete=models.CASCADE)
	end_location = models.ForeignKey(Address, related_name='end_address', on_delete=models.CASCADE)
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






