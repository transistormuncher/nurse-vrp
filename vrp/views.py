from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Address
import subprocess
import pandas as pd


# Create your views here.
from django.http import HttpResponse
from .exports import generate_stop_csv






def index(request):
    context = {'msg': 'Welcome'}
    return render(request, 'vrp/index.html', context)


# test export
def export(request):
	generate_stop_csv()
	return HttpResponse("Hello world, you exported the addresses.")

# debug
def show(request):
	my_list = []
	df = pd.read_csv("data/dist_matrix.csv")
	for i in df.index:
		my_list.append([ df.iloc[i,1], df.iloc[i,2], df.iloc[i,3]])
	
	context = {'object_list': my_list}
	return render(request, 'vrp/show.html', context)

# java test
def java(request):
	# subprocess.call(['java', '-jar', 'hello.jar', "argument-1", "argument-2"])
	subprocess.Popen(['java', '-jar', 'graphhopper/graphhopper-web-0.9.0-with-dep.jar', "jetty.resourcebase=webapp", "config=graphhopper/config-example.properties", "datareader.file=graphhopper/slovakia-latest.osm.pbf"])
	context = {'msg': "ran java"}
	return render(request, 'vrp/index.html', context)



### address views

# old
def address_list(request):
    addresses = Address.objects.all()
    return render_to_response('vrp/address_list.html', {'object_list': addresses})


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



