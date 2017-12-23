from xml.dom.minidom import parse
import xml.dom.minidom
import re
from .models import Route, Stop, Vehicle, Address



def create_routes(tour):
	# Open XML document using minidom parser
	DOMTree = xml.dom.minidom.parse("data/vrp_output/solution_tour[{}].xml".format(tour.id))
	solutions = DOMTree.documentElement
	s = solutions.getElementsByTagName("solution")[0]
	routes = s.getElementsByTagName("route")
	p = re.compile('\d+$')

	route_counter = 0
	for route in routes:
		route_counter += 1
		print ("*****Route*****")
		v = route.getElementsByTagName('vehicleId')[0]
		print(v.childNodes[0].data)
		v_id = p.search(v.childNodes[0].data)[0]
    	


		route_obj, created = Route.objects.update_or_create(
				route_number= route_counter,
				tour=tour,
				vehicle=Vehicle.objects.get(pk=v_id),
				defaults={
				'distance': 0,
				'duration': 0
					}
					)
		print(route_obj)
		print("created: %s" % created)

		stop_counter = 0

		stop_obj, created = Stop.objects.update_or_create(
				address=Address.objects.get(pk=tour.start_location.id),
				route=route_obj,
				sequence= stop_counter)


		actions = route.getElementsByTagName('act')
		for a in actions:
			stop_counter += 1
			stop_id = a.getElementsByTagName('serviceId')[0]
			print(stop_id.childNodes[0].data)

			stop_obj, created = Stop.objects.update_or_create(
				address=Address.objects.get(pk=stop_id.childNodes[0].data),
				route=route_obj,
				sequence= stop_counter)

			print(stop_obj)
			print("created: %s" % created)

		stop_counter += 1

		stop_obj, created = Stop.objects.update_or_create(
				address=Address.objects.get(pk=tour.end_location.id),
				route=route_obj,
				sequence= stop_counter)

	print(tour.date)
	return