from django.urls import path
from . import views
# from django.conf.urls import url
from .views import ListView, SearchResultsView

app_name = 'catalog'
urlpatterns = [
    path('', views.index, name='index1'),
    path('search/', SearchResultsView.as_view(), name='search_result'),
    path(r'^inventorys/$', views.InventoryListView.as_view(), name='inventory'),
    path(r'^devices/$', views.DeviceListView.as_view(), name='devices'),
    path(r'^device/(?P<pk>\d+)$', views.DeviceDetailView.as_view(), name='device-detail'),
    path(r'^customers/$', views.CustomerListView.as_view(), name='customers'),
    path(r'^customer/(?P<pk>\d+)$', views.CustomerDetailView.as_view(), name='customer_detail'),
    path(r'^trackers/$', views.TrackerListView.as_view(), name='trackers'),
    path(r'^tracker/(?P<pk>\d+)$', views.TrackerDetailView.as_view(), name='tracker_detail'),

]