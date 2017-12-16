import urllib3
import pandas as pd
import json
from pandas.io.json import json_normalize  
import urllib.parse


def distance(x1, y1, x2, y2):
	http = urllib3.PoolManager()
	point1 = str(x1) + "%2C" + str(y1)
	point2 = str(x2) + "%2C" + str(y2)
	request = http.request('GET','http://localhost:8989/route?point=' +point1 + '&point='+point2 +'&calc_points=false')
	data = json.loads(request.data)
	resp = json_normalize(data, "paths")
	distance = round(resp.iloc[0,0]/1000, 3)
	time = round(resp.iloc[0,2]/60000, 2)
	return(distance, time)



def create_matrix(modeladmin, request, queryset):
	if not os.path.exists("data"):
		os.makedirs("data")
	mylist = []
	for i in queryset:
		for j in queryset:
			if not i ==j:
				dist, time = distance(i.latitude, i.longitude, j.latitude, j.longitude)
				mylist.append([i.name, j.name, dist, time])
	dist_matrix = pd.DataFrame(mylist)
	dist_matrix.to_csv("data/dist_matrix.csv")
create_matrix.short_description = "Create distance matrix"


