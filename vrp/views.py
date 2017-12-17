from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import *
import subprocess
import pandas as pd


# Create your views here.
from django.http import HttpResponse
from .exports import *






def index(request):
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

# java test
def java(request):
	subprocess.Popen(['java', '-jar', 'hello.jar', "argument-1", "argument-2"])
	# subprocess.Popen(['java', '-jar', 'graphhopper/graphhopper-web-0.9.0-with-dep.jar', "jetty.resourcebase=webapp", "config=graphhopper/config-example.properties", "datareader.file=graphhopper/slovakia-latest.osm.pbf"])
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
	tour = Tour.objects.get(pk=pk)
	addresses = tour.stops.all()

	export_points(tour)
	f_in = "data/points_for_dist_mat_[tour_{}].csv".format(pk)
	f_out = "data/dist_mat_[tour_{}].csv".format(pk)
	gh_folder = "data/gh_data"

	subprocess.Popen(['java', '-jar', 'java/gh_module.jar', f_in, f_out, gh_folder])
	# gen distmat
	# export addresses for service
	# export vehicles
	# start calculation
	context = {'object': tour, 'addresses': addresses}
	return render(request, 'vrp/tour_calculate.html', context)




