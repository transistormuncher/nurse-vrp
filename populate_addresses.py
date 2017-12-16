#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import django
from decimal import Decimal

import pandas as pd

os.environ["DJANGO_SETTINGS_MODULE"] = 'routing.settings'
django.setup()

from vrp.models import Address

addresses = pd.read_csv("test_addresses2.csv")

for i in addresses.index:
	obj, created = Address.objects.update_or_create(
		name=addresses.iloc[i,1],
		latitude=addresses.iloc[i,2],
		longitude=addresses.iloc[i,3],
		defaults={
		'street': 'test-street'
		}
		)
	print(obj)
	print("created: %s" % created)

addresses.to_csv("data/stop_list_test.csv")




