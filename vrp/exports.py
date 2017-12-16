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
