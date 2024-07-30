from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
'''from .views import DeviceViewSet, CustomerViewSet, ModelViewSet, TrackerViewSet, InventoryViewSet'''
from .views import ListView

from .views import AssetListView, AssetDetailView, AssetCreateView, AssetUpdateView, AssetDeleteView

from .views import CustomLoginView, CustomSignupView, TemplateView  # Import the signup view
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views
from .views import ReturnAssetView, ReturnAssetSuccessView, MaintenanceListView, FixDamagedAssetView


'''
# Set up the router for API endpoints
router = DefaultRouter()
router.register(r'devices', DeviceViewSet)
router.register(r'customers', CustomerViewSet)
router.register(r'models', ModelViewSet)
router.register(r'trackers', TrackerViewSet)
router.register(r'inventories', InventoryViewSet)
'''
app_name = 'catalog'

urlpatterns = [
    # API endpoints

    # Class-based views
    path('', CustomLoginView.as_view(), name='login'),  # Set login page as default
    path('home/', views.index, name='index1'),  # Home page after login


    path('assets/', AssetListView.as_view(), name='asset-list'),
    path('assets/create/', AssetCreateView.as_view(), name='asset_create'),
    path('assets/<str:pk>/update/', views.AssetUpdateView.as_view(), name='asset-update'),
    path('assets/<str:pk>/delete/', views.AssetDeleteView.as_view(), name='asset-delete'),
    path('assets/<str:pk>/', views.AssetDetailView.as_view(), name='asset-detail'),

    # Add URLs for Employee, AssetAssignment, UsageHistory, and Maintenance
    path('login/', CustomLoginView.as_view(), name='login'),  # Login page URL
    path('logout/', LogoutView.as_view(next_page='catalog:login'), name='logout'),
    path('signup/', CustomSignupView.as_view(), name='signup'),

    path('password_reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),


    path('assign-asset/', views.assign_asset, name='assign_asset'),
    path('assign/success/', views.assign_asset_success, name='assign_asset_success'),
    path('assigned-assets/', views.asset_assignment_list, name='assigned_asset_list'),  # New URL pattern


    path('asset-assignment/return/<int:pk>/', ReturnAssetView.as_view(), name='return_asset'),
    path('maintenance/', MaintenanceListView.as_view(), name='maintenance-list'),
    path('return-asset-success/', TemplateView.as_view(template_name='catalog/return_asset_success.html'), name='return_asset_success'),
    path('maintenance/fix/<int:pk>/', FixDamagedAssetView.as_view(), name='fix_damaged_asset'),


]







