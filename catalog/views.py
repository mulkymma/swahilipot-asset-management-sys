from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator
from django.views.generic import ListView, TemplateView
from django.db.models import Count, Q
'''from .models import Device, Customer, Model, Tracker, Inventory'''
from django.views import generic
from django.urls import reverse, reverse_lazy
from rest_framework import viewsets
'''from .serializers import DeviceSerializer, CustomerSerializer, ModelSerializer, TrackerSerializer, InventorySerializer'''

from .models import Asset
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib import messages
from .forms import CustomUserCreationForm
from .forms import AssetAssignmentForm, ReturnAssetForm
from django.shortcuts import render, redirect
from .models import AssignedAsset, AssetAssignment, DamagedAsset
from django.views import View
from django.utils import timezone
from .forms import FixDamagedAssetForm


from django.core.files.base import ContentFile
from io import BytesIO
import qrcode



class CustomLoginView(LoginView):
    template_name = 'catalog/login.html'
    
'''
class CustomLoginView(LoginView):
    template_name = 'catalog/login.html'
    success_url = reverse_lazy('asset-list')'''
class CustomSignupView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'catalog/signup.html'
    success_url = reverse_lazy('catalog:login')  # Redirects to login page

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()
        
        # Authenticate and log in the user
        user = authenticate(username=user.username, password=form.cleaned_data['password1'])
        if user is not None:
            login(self.request, user)
            messages.success(self.request, 'Sign up successful! You are now logged in.')
        else:
            messages.error(self.request, 'Sign up failed. Please try again.')
        return response
    
def asset_assignment_list(request):
    asset_assignment = AssetAssignment.objects.all()
    return render(request, 'catalog/asset_assignment_list.html', {'asset_assignment': asset_assignment })



class ReturnAssetView(View):
    template_name = 'catalog/return_asset.html'

    def get(self, request, pk, *args, **kwargs):
        asset_assignment = get_object_or_404(AssetAssignment, pk=pk)
        form = ReturnAssetForm(asset_assignment=asset_assignment)
        return render(request, self.template_name, {'form': form, 'asset_assignment': asset_assignment})

    def post(self, request, pk, *args, **kwargs):
        asset_assignment = get_object_or_404(AssetAssignment, pk=pk)
        form = ReturnAssetForm(request.POST, asset_assignment=asset_assignment)
        if form.is_valid():
            quantity_good = form.cleaned_data['quantity_good']
            quantity_damaged = form.cleaned_data['quantity_damaged']

            asset_assignment.quantity -= (quantity_good + quantity_damaged)
            if asset_assignment.quantity <= 0:
                asset_assignment.delete()
            else:
                asset_assignment.save()

            asset = asset_assignment.asset
            asset.quantity += quantity_good
            asset.save()

            if quantity_damaged > 0:
                DamagedAsset.objects.create(
                    asset=asset,
                    quantity=quantity_damaged,
                    date_reported=timezone.now()

                )

            return redirect('catalog:return_asset_success')

        return render(request, self.template_name, {'form': form, 'asset_assignment': asset_assignment})
    
class ReturnAssetSuccessView(TemplateView):
    template_name = 'return_asset_success.html'



class MaintenanceListView(View):
    template_name = 'catalog/maintenance_list.html'

    def get(self, request, *args, **kwargs):
        damaged_assets = DamagedAsset.objects.all()
        return render(request, self.template_name, {'damaged_assets': damaged_assets})



class FixDamagedAssetView(View):
    template_name = 'catalog/fix_damaged_asset.html'

    def get(self, request, pk, *args, **kwargs):
        damaged_asset = get_object_or_404(DamagedAsset, pk=pk)
        form = FixDamagedAssetForm(instance=damaged_asset)
        return render(request, self.template_name, {'form': form, 'damaged_asset': damaged_asset})

    def post(self, request, pk, *args, **kwargs):
        damaged_asset = get_object_or_404(DamagedAsset, pk=pk)
        form = FixDamagedAssetForm(request.POST, instance=damaged_asset)
        if form.is_valid():
            asset = damaged_asset.asset
            asset.quantity += damaged_asset.quantity
            asset.save()
            damaged_asset.delete()
            return redirect('catalog:maintenance-list')

        return render(request, self.template_name, {'form': form, 'damaged_asset': damaged_asset})
    


def generate_qr_code(data):
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    byte_io = BytesIO()
    img.save(byte_io, format='PNG')
    return ContentFile(byte_io.getvalue(), 'asset_qr_code.png')



class CustomPasswordResetView(PasswordResetView):
    template_name = 'catalog/password_reset_form.html'
    email_template_name = 'catalog/password_reset_email.html'
    success_url = reverse_lazy('catalog:password_reset_done')

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'catalog/password_reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'catalog/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'catalog/password_reset_complete.html'




def assign_asset(request):
    if request.method == 'POST':
        form = AssetAssignmentForm(request.POST)
        if form.is_valid():
            asset_assignment = form.save(commit=False)
            asset = asset_assignment.asset
            
            if asset.quantity >= asset_assignment.quantity:
                asset.quantity -= asset_assignment.quantity
                asset.save()
                asset_assignment.save()
                return redirect('catalog:assign_asset_success')
            else:
                form.add_error('quantity', 'Not enough assets available for this assignment.')
    else:
        form = AssetAssignmentForm()
    
    return render(request, 'catalog/assign_asset.html', {'form': form})

def assign_asset_success(request):
    return render(request, 'catalog/assign_asset_success.html')


class AssetListView(ListView):
    model = Asset
    template_name = 'catalog/asset_list.html'
    context_object_name = 'asset'

class AssetDetailView(DetailView):
    model = Asset
    template_name = 'catalog/asset_detail.html'
    context_object_name = 'asset'

    if not Asset.qr_code:
        qr_code_image = generate_qr_code(Asset.id)
        Asset.qr_code.save('asset_qr_code.png', qr_code_image, save=True)

    def get_object(self):
        """Override get_object to lookup by custom id field"""
        pk = self.kwargs.get('pk')
        return get_object_or_404(Asset, id=pk)


class AssetCreateView(CreateView):
    model = Asset
    fields = ['name', 'quantity', 'category', 'location', 'condition']
    template_name = 'catalog/asset_create.html'
    success_url = reverse_lazy('catalog:asset-list')

class AssetUpdateView(UpdateView):
    model = Asset
    fields = ['name', 'category', 'location', 'condition', 'quantity']
    template_name = 'catalog/asset_form.html'
    success_url = reverse_lazy('catalog:asset-list')

    def get_object(self, queryset=None):
        """Override get_object to lookup by custom id field"""
        pk = self.kwargs.get('pk')
        return get_object_or_404(Asset, id=pk)

class AssetDeleteView(DeleteView):
    model = Asset
    template_name = 'catalog/asset_confirm_delete.html'
    success_url = reverse_lazy('catalog:asset-list')

    def get_object(self, queryset=None):
        """Override get_object to lookup by custom id field"""
        pk = self.kwargs.get('pk')
        return get_object_or_404(Asset, id=pk)


def asset_list(request):
    assets = Asset.objects.all()
    assets_by_type = {}
    for asset in assets:
        assets_by_type.setdefault(asset.type, []).append(asset)

    return render(request, 'catalog/asset_list.html', {'assets_by_type': assets_by_type})

class AssetDetailView(DetailView):
    model = Asset
    template_name = 'catalog/asset_detail.html'
    context_object_name = 'asset'





def index(request):
    """
    Index page with count stock
    """
    # Count total assets
    num_assets = Asset.objects.count()

    # Count assigned assets
    num_assigned_assets = AssetAssignment.objects.count()

    # Count damaged assets
    num_damaged_assets = DamagedAsset.objects.count()

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    # Render HTML-template index.html with data
    return render(
        request,
        'index1.html',
        context={
            'num_assets': num_assets,
            'num_assigned_assets': num_assigned_assets,
            'num_damaged_assets': num_damaged_assets,
            'num_visits': num_visits,
        },
    )

'''

# API ViewSets
class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class ModelViewSet(viewsets.ModelViewSet):
    queryset = Model.objects.all()
    serializer_class = ModelSerializer

class TrackerViewSet(viewsets.ModelViewSet):
    queryset = Tracker.objects.all()
    serializer_class = TrackerSerializer

class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer


""" Device List view """
class DeviceListView(generic.ListView):
    model = Device
    context_object_name = 'device_list'   # ваше собственное имя переменной контекста в шаблоне
    list_display = ('title', 'display_model', 'customer', 'display_status', 'serialn', 'substatus', 'tag')
    queryset = Device.objects.all()
    template_name = 'catalog/device_list.html'


    def get_queryset(self):
        return Device.objects.all()

""" Device detail view """
class DeviceDetailView(generic.DetailView):
    model = Device

    def device_detail_view(request, pk):
        try:
            device_id = Device.objects.get(pk=pk)
        except Device.DoesNotExist:
            raise Http404("Device does not exist")

        return render(
            request,
            'catalog/device_detail.html',
            context={'device': device_id, }
        )

""" Customer list view """
class CustomerListView(generic.ListView):
    model = Customer
    context_object_name = 'customer_list'   # ваше собственное имя переменной контекста в шаблоне
    list_display = ('last_name', 'first_name', 'department', 'location')
    queryset = Customer.objects.all()
    template_name = 'catalog/customer_list.html'
    paginate_by = 30

    def get_queryset(self):
        return Customer.objects.all()

""" Customer detail view """
class CustomerDetailView(generic.DetailView):
    model = Customer
    context_object_name = 'customer'
    template_name = 'catalog/customer_detail.html'

    def get_queryset(self):
        return Customer.objects.all()

    def get_context_data(self, **kwargs):
        cid = get_object_or_404(Customer, pk=self.kwargs['pk'])
        context = super().get_context_data(**kwargs)
        context['customer_detail'] = Device.objects.filter(customer_id=cid)
        return context


""" Tracker list view """
class TrackerListView(generic.ListView):
    model = Tracker
    context_object_name = 'tracker_list'
    template_name = 'catalog/tracker_list.html'
    paginate_by = 30


""" Tracker detail view """
class TrackerDetailView(generic.DetailView):
    model = Tracker
    context_object_name = 'tracker'


    template_name = 'catalog/tracker_detail.html'
    def get_queryset(self):
        return Tracker.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tracker_listkz'] = Customer.objects.all()
        return context

""" Search view """
class SearchResultsView(generic.ListView):
    model = Device
    template_name = 'search_result.html'


    def get_queryset(self):  # новый
        query = self.request.GET.get('q')
        object_list = Device.objects.filter( Q(status__icontains=query) |
                                            Q(serialn__icontains=query) | Q(customer__last_name__icontains=query) | Q(model__name__icontains=query))
        return object_list

""" Inventory data view """
class InventoryListView(generic.ListView):
    model = Inventory
    context_object_name = 'object_list'
    template_name = 'inv.html'
    paginate_by = 48

'''

