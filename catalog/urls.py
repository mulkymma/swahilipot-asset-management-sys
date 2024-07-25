from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import DeviceViewSet, CustomerViewSet, ModelViewSet, TrackerViewSet, InventoryViewSet
from .views import ListView, SearchResultsView

from .views import AssetListView, AssetDetailView, AssetCreateView, AssetUpdateView, AssetDeleteView

from .views import CustomLoginView



# Set up the router for API endpoints
router = DefaultRouter()
router.register(r'devices', DeviceViewSet)
router.register(r'customers', CustomerViewSet)
router.register(r'models', ModelViewSet)
router.register(r'trackers', TrackerViewSet)
router.register(r'inventories', InventoryViewSet)

app_name = 'catalog'

urlpatterns = [
    # API endpoints
    path('api/', include(router.urls)),

    # Class-based views
    path('', views.index, name='index1'),
    path('search/', SearchResultsView.as_view(), name='search_result'),
    path('inventory/', views.InventoryListView.as_view(), name='inventory'),
    path('devices/', views.DeviceListView.as_view(), name='devices'),
    path('device/<int:pk>/', views.DeviceDetailView.as_view(), name='device-detail'),
    path('customers/', views.CustomerListView.as_view(), name='customers'),
    path('customer/<int:pk>/', views.CustomerDetailView.as_view(), name='customer_detail'),
    path('trackers/', views.TrackerListView.as_view(), name='trackers'),
    path('tracker/<int:pk>/', views.TrackerDetailView.as_view(), name='tracker_detail'),


    path('assets/', AssetListView.as_view(), name='asset-list'),
    path('assets/<int:pk>/', AssetDetailView.as_view(), name='asset-detail'),
    path('assets/create/', AssetCreateView.as_view(), name='asset-create'),
    path('assets/<int:pk>/update/', AssetUpdateView.as_view(), name='asset-update'),
    path('assets/<int:pk>/delete/', AssetDeleteView.as_view(), name='asset-delete'),
    path('assets/', AssetListView.as_view(), name='asset-list'),
    path('assets/<int:pk>/', AssetDetailView.as_view(), name='asset-detail'),
    path('assets/create/', AssetCreateView.as_view(), name='asset-create'),
    path('assets/<int:pk>/update/', AssetUpdateView.as_view(), name='asset-update'),
    path('assets/<int:pk>/delete/', AssetDeleteView.as_view(), name='asset-delete'),



    # Add URLs for Employee, AssetAssignment, UsageHistory, and Maintenance
    path('accounts/login/', CustomLoginView.as_view(template_name='registration/login.html'), name='login'),

]
