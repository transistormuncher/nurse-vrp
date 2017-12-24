from django.conf.urls import url

from .views import *

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^export$', export, name='export'),
    url(r'^java$', java, name='java'),
    url(r'^show/(?P<pk>\d+)$', show, name='showing'),
    url(r'^show_vrp/(?P<pk>\d+)$', show, name='show_vrp'),

    url(r'^address/$', AddressListView.as_view(), name='address-list'),
    url(r'^address/(?P<pk>\d+)$', AddressDetailView.as_view(), name='address-detail'),
    url(r'^address/create$', AddressCreateView.as_view(), name='address-create'),
    url(r'^address/(?P<pk>\d+)/update$', AddressUpdateView.as_view(), name='address-update'),
    url(r'^address/remove_address/(?P<pk>\d+)/$', AddressDeleteView.as_view(), name='address-delete'),

    url(r'^vehicle/$', VehicleListView.as_view(), name='vehicle-list'),
    url(r'^vehicle/(?P<pk>\d+)$', VehicleDetailView.as_view(), name='vehicle-detail'),
    url(r'^vehicle/create$', VehicleCreateView.as_view(), name='vehicle-create'),
    url(r'^vehicle/(?P<pk>\d+)/update$', VehicleUpdateView.as_view(), name='vehicle-update'),
    url(r'^vehicle/remove_vehicle/(?P<pk>\d+)/$', VehicleDeleteView.as_view(), name='vehicle-delete'),

    url(r'^tour/$', TourListView.as_view(), name='tour-list'),
    url(r'^tour/(?P<pk>\d+)$', TourDetailView.as_view(), name='tour-detail'),
    url(r'^tour/create$', TourCreateView.as_view(), name='tour-create'),
    url(r'^tour/(?P<pk>\d+)/update$', TourUpdateView.as_view(), name='tour-update'),
    url(r'^tour/remove_tour/(?P<pk>\d+)/$', TourDeleteView.as_view(), name='tour-delete'),
    url(r'^tour/(?P<pk>\d+)/calculate$', tour_calculate, name='tour-calculate'),
    url(r'^tour/(?P<pk>\d+)/routes$', tour_show_routes, name='show-routes'),




]