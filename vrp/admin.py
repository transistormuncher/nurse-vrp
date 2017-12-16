from django.contrib import admin
from.models import *
import pandas as pd
from .exports import export_selected_addresses
from .distance_matrix import create_matrix

# Register your models here.

def export_addresses2(modeladmin, request, queryset):
	mylist = []
	for o in queryset:
		print(o.name)
		mylist.append([o.name,o.latitude,o.longitude])
		export = pd.DataFrame(mylist)
		export.to_csv("admin_export.csv")
export_addresses2.short_description = "Export selected addresses"



class AddressAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'latitude', 'longitude')
    actions = [export_selected_addresses, create_matrix]

class TourAdmin(admin.ModelAdmin):
	list_display = ['date']
	filter_horizontal = ['stops']



admin.site.register(Address, AddressAdmin)

admin.site.register(Tour, TourAdmin)
admin.site.register(Vehicle)