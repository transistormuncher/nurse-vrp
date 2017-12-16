from django.conf.urls import url

from .views import *

urlpatterns = [
    url(r'^index$', index, name='index'),
    url(r'^export$', export, name='export'),
    url(r'^java$', java, name='java'),
    url(r'^show$', show, name='showing'),
    url(r'^address_old/$', address_list, name='address-list-old'),
    url(r'^address/$', AddressListView.as_view(), name='address-list'),
    url(r'^address/(?P<pk>\d+)$', AddressDetailView.as_view(), name='address-detail'),
    url(r'^address/create$', AddressCreateView.as_view(), name='address-create'),
    url(r'^address/(?P<pk>\d+)/update$', AddressUpdateView.as_view(), name='address-update'),
    url(r'^address/remove_address/(?P<pk>\d+)/$', AddressDeleteView.as_view(), name='address-delete')

]