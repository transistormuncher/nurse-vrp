from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import *
import subprocess
import pandas as pd
from decimal import Decimal
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


# Create your views here.
from django.http import HttpResponse
from .exports import *






def index(request):
	"""Preliminary Index Site"""

	context = {'msg': 'Welcome'}
	return render(request, 'vrp/index.html', context)


# test export
def export(request):
	generate_stop_csv()
	return HttpResponse("Hello world, you exported the addresses.")

# debug
def show(request, pk):
	my_list = []
	df = pd.read_csv("data/dist_mat_[tour_{}].csv".format(pk))
	for i in df.index:
		my_list.append([df.iloc[i,0], df.iloc[i,1], df.iloc[i,2], df.iloc[i,3]])
	
	context = {'object_list': my_list}
	return render(request, 'vrp/show.html', context)

# debug
def show_vrp(request, pk):
	my_list = []
	df = pd.read_csv("data/dist_mat_[tour_{}].csv".format(pk))
	for i in df.index:
		my_list.append([df.iloc[i,0], df.iloc[i,1], df.iloc[i,2], df.iloc[i,3]])
	
	context = {'object_list': my_list}
	return render(request, 'vrp/show.html', context)


# java test
def java(request):
	"""Test call to a java jar"""
	subprocess.Popen(['java', '-jar', 'hello.jar', "argument-1", "argument-2"])
	context = {'msg': "ran java"}
	return render(request, 'vrp/index.html', context)



### Address Views

class AddressListView(ListView):
    model = Address
    paginate_by = 5

class AddressDetailView(DetailView):
    model = Address

class AddressCreateView(CreateView):
    model = Address
    fields = ["name", "street", "housenumber",  "postcode", "city", "country", "latitude", "longitude" ]

class AddressUpdateView(UpdateView):
    model = Address
    fields = ["name", "street", "housenumber",  "postcode", "city", "country", "latitude", "longitude" ]
    template_name = "vrp/address_update_form.html"

class AddressDeleteView(DeleteView):
    model = Address

    def get_success_url(self):
    	return reverse('address-list')


### Vehicle Views

class VehicleListView(ListView):
    model = Vehicle

class VehicleDetailView(DetailView):
    model = Vehicle

class VehicleCreateView(CreateView):
    model = Vehicle
    fields = ["name", "capacity", "fuel_consumption", "notes", ]

class VehicleUpdateView(UpdateView):
    model = Vehicle
    fields = ["name", "capacity", "fuel_consumption", "notes", ]
    template_name = "vrp/vehicle_update_form.html"

class VehicleDeleteView(DeleteView):
    model = Vehicle

    def get_success_url(self):
    	return reverse('vehicle-list')



### Tour Views

class TourListView(ListView):
    model = Tour

class TourDetailView(DetailView):
    model = Tour

class TourCreateView(CreateView):
    model = Tour
    form_class = TourForm
    # fields = ["date", "start_location", "end_location", "stops", "vehicles", "drivers", "notes", ]

class TourUpdateView(UpdateView):
    model = Tour
    form_class = TourForm
    # fields = ["date", "start_location", "end_location", "stops", "vehicles", "drivers", "notes", ]
    template_name = "vrp/tour_update_form.html"

class TourDeleteView(DeleteView):
    model = Tour

    def get_success_url(self):
    	return reverse('tour-list')

def tour_calculate(request, pk):
	"""Calculates the optimal solution for a tour"""
	tour = Tour.objects.get(pk=pk)
	addresses = tour.stops.all()

	# delete previously existing files:
	filename = "data/vrp_output/solution_tour[{}].xml".format(pk)
	if os.path.exists(filename):
		os.remove(filename) 

	# export points (for dist mat and services)
	export_points(tour)
	export_vehicles(tour)
	
	# gen distmat
	f_in = "data/points_for_[tour_{}].csv".format(pk)
	f_out = "data/dist_mat_[tour_{}].csv".format(pk)
	# clean old files
	if os.path.exists(f_out):
		os.remove(f_out) 
	gh_folder = "data/gh_data"
	p = subprocess.Popen(['java', '-jar', 'java/gh_module.jar', f_in, f_out, gh_folder])

	# start calculation
	context = {'object': tour, 'addresses': addresses}
	return render(request, 'vrp/tour_calculate.html', context)


def tour_show_routes(request, pk):
	"""Calculates the optimal solution for a tour"""
	tour = Tour.objects.get(pk=pk)
	tour.parse_xml()
	routes = tour.route_set.all()
	#TODO calculate routes in ghopper
	dist_mat = pd.read_csv("data/dist_mat_[tour_{}].csv".format(pk))
	dist_mat["distance"] = round(dist_mat["distance"]/1000,2)
	dist_mat["distance"] = dist_mat["distance"].apply(Decimal)
	dist_mat["duration"] = dist_mat["duration"].apply(Decimal)

	print(dist_mat)

	for r in routes:
		stops = r.stop_set.all()
		length = stops.count()
		for i in range(1,length):
			stop = stops[i]
			from_id = stops[i-1].address.id
			to_id = stop.address.id
			print(stops[i-1].address.id, stop.address.id)
			print(dist_mat[(dist_mat["from id"] == from_id) & (dist_mat["to id"] == to_id)])
			print(dist_mat[(dist_mat["from id"] == from_id) & (dist_mat["to id"] == to_id)]["distance"])
			stop.distance = dist_mat[(dist_mat["from id"] == from_id) & (dist_mat["to id"] == to_id)]["distance"].values[0] 
			stop.duration = dist_mat[(dist_mat["from id"] == from_id) & (dist_mat["to id"] == to_id)]["duration"].values[0]
			stop.save(update_fields=['distance', 'duration'])
			print(stop.distance, stop.duration)




	context = {'tour': tour, 'routes': routes}

	return render(request, 'vrp/show_routes.html', context)



def tour_send_routes_old(request, pk):
	tour = Tour.objects.get(pk=pk)
	routes = tour.route_set.all()
	msg = "Hallo Olli,\nthese are the routes:\n\n"
	for r in routes:
		msg += "*" + r.__str__() + ":*\n"

	subject = "Tour Plan"
	res = send_mail(subject, msg, "novaky.nurse@gmail.com", ["oliver.folba@gmail.com"])
	return HttpResponse('%s'%res)

def tour_send_routes(request, pk):
	tour = Tour.objects.get(pk=pk)
	routes = tour.route_set.all()
	subject, from_email, to = '{} Plan'.format(tour), 'novaky.nurse@gmail.com', 'oliver.folba@gmail.com'
	html_content = render_to_string('vrp/tour_email.html', {'tour': tour, 'routes': routes}) # ...
	text_content = strip_tags(html_content) # this strips the html, so people will have the text as well.
	# create the email, and attach the HTML version as well.
	msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
	msg.attach_alternative(html_content, "text/html")
	msg.send()
	context = {"msg": "Email sent"}
	return render(request, 'vrp/index.html', context)






