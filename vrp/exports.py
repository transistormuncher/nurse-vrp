import pandas as pd
import os
from .models import Address	


def generate_stop_csv():

	if not os.path.exists("data"):
		os.makedirs("data")
	mylist = []
	for o in Address.objects.all():
		print(o.name)
		mylist.append([o.name,o.latitude,o.longitude])
	export = pd.DataFrame(mylist)
	export.to_csv("data/stop_list_2.csv")
	return


def export_selected_addresses(modeladmin, request, queryset):
	mylist = []
	for o in queryset:
		print(o.name)
		mylist.append([o.name,o.latitude,o.longitude])
		export = pd.DataFrame(mylist)
		export.to_csv("data/admin_export2.csv")
export_selected_addresses.short_description = "Export selected addresses"


def export_points(tour):
	mylist = []
	s = tour.start_location
	e = tour.end_location
	stops = tour.stops.all()

	mylist.append(["start", s.id, s.name, s.latitude, s.longitude])
	i = 0
	for stop in stops:
		i+=1
		mylist.append(["stop_{}".format(i), stop.id, stop.name, stop.latitude, stop.longitude])
	mylist.append(["end", e.id, e.name, e.latitude, e.longitude])
	export = pd.DataFrame(mylist, columns = ["function", "id", "name", "lat", "lon"])
	fname = "data/points_for_dist_mat_[tour_{}].csv".format(tour.id)
	export.to_csv(fname, header=True, index=False)

	return

