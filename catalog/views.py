from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.views.generic import ListView
from django.db.models import Count, Q
from .models import Device, Customer, Model, Tracker, Inventory
from django.views import generic
from django.urls import reverse, reverse_lazy
from rest_framework import viewsets
from .serializers import DeviceSerializer, CustomerSerializer, ModelSerializer, TrackerSerializer, InventorySerializer

from .models import Asset
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from django.contrib.auth.views import LoginView

class CustomLoginView(LoginView):
    template_name = 'catalog/login.html'
    success_url = reverse_lazy('asset-list')




class AssetListView(ListView):
    model = Asset
    template_name = 'catalog/asset_list.html'
    context_object_name = 'asset'

class AssetDetailView(DetailView):
    model = Asset
    template_name = 'catalog/asset_detail.html'
    context_object_name = 'asset'

    def get(self, request, *args, **kwargs):
        print(f"Asset ID: {kwargs['pk']}")
        response = super().get(request, *args, **kwargs)
        print(f"Asset Object: {self.get_object()}")
        return response


class AssetCreateView(CreateView):
    model = Asset
    fields = ['name', 'category', 'location', 'condition']
    template_name = 'catalog/asset_form.html'
    success_url = reverse_lazy('asset-list')

class AssetUpdateView(UpdateView):
    model = Asset
    fields = ['name', 'category', 'location', 'condition']
    template_name = 'catalog/asset_form.html'
    success_url = reverse_lazy('asset-list')

class AssetDeleteView(DeleteView):
    model = Asset
    template_name = 'catalog/asset_confirm_delete.html'
    success_url = reverse_lazy('asset-list')


def asset_list(request):
    assets = Asset.objects.all()
    assets_by_type = {}
    for asset in assets:
        assets_by_type.setdefault(asset.type, []).append(asset)

    return render(request, 'catalog/asset_list.html', {'assets_by_type': assets_by_type})












# Create your views here.
def index(request):
    """
    Index page with count stock
    """
    #  "Count some devices
    num_devices=Device.objects.all().count()
    num_lt=Device.objects.filter(type__exact='3').count()
    num_dl_dep=Device.objects.filter(type__exact='3', status__exact='1').count()
    num_dv_new=Device.objects.filter(status__exact='0').count()
    num_dv_stk=Device.objects.filter(status__exact='3').count()
    num_dt = Device.objects.filter(type__exact='2').count()
    num_mt = Device.objects.filter(type__exact='9').count()

    num_authors=Customer.objects.count()
    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    # view HTML-template index.html with data
    # variable context
    return render(
           request,
        'index1.html',
        context={
            'num_devices': num_devices,
            'num_authors': num_authors,
            'num_visits': num_visits,
            'num_lt': num_lt,
            'num_dt': num_dt,
            'num_mt': num_mt,
            'num_dl_dep': num_dl_dep,
            'num_dv_stk': num_dv_stk,
            'num_dv_new': num_dv_new
        },
    )
    reverse('catalog_index1', args=())

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