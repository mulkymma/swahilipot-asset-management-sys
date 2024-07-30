from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Asset, AssetAssignment
from .models import DamagedAsset



class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email is already in use.')
        return email
    

class AssetAssignmentForm(forms.ModelForm):
    asset = forms.ModelChoiceField(queryset=Asset.objects.all(), empty_label="Select an Asset", widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = AssetAssignment
        fields = ['asset', 'quantity', 'organisation_name', 'phone_number', 'date_picked', 'date_to_return']
        widgets = {
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'organisation_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'date_picked': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'date_to_return': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class ReturnAssetForm(forms.ModelForm):
    asset = forms.ModelChoiceField(queryset=Asset.objects.all(), widget=forms.Select(attrs={'readonly': 'readonly'}))
    quantity = forms.IntegerField(widget=forms.NumberInput(attrs={'readonly': 'readonly'}), label="Quantity Assigned")
    quantity_good = forms.IntegerField(min_value=0, label="Quantity in Good Condition")
    quantity_damaged = forms.IntegerField(min_value=0, label="Quantity Damaged")
    organisation_name = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))

    class Meta:
        model = AssetAssignment
        fields = ['asset', 'quantity', 'organisation_name', 'phone_number','quantity_good', 'quantity_damaged', ]

    def __init__(self, *args, **kwargs):
        asset_assignment = kwargs.pop('asset_assignment', None)
        super().__init__(*args, **kwargs)
        if asset_assignment:
            self.fields['organisation_name'].initial = asset_assignment.organisation_name
            self.fields['phone_number'].initial = asset_assignment.phone_number
            self.fields['asset'].initial = asset_assignment.asset
            self.fields['quantity'].initial = asset_assignment.quantity
            self.asset_assignment = asset_assignment

    def clean(self):
        cleaned_data = super().clean()
        quantity_good = cleaned_data.get("quantity_good")
        quantity_damaged = cleaned_data.get("quantity_damaged")

        if quantity_good is not None and quantity_damaged is not None:
            if quantity_good + quantity_damaged > self.asset_assignment.quantity:
                raise forms.ValidationError("Returned quantity cannot exceed the assigned quantity.")
            



class FixDamagedAssetForm(forms.ModelForm):
    class Meta:
        model = DamagedAsset
        fields = ['asset', 'quantity']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['asset'].widget.attrs['readonly'] = True
        self.fields['quantity'].widget.attrs['readonly'] = True