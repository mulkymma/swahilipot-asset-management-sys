from django import forms
from ..catalog.models import Asset

class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['name', 'category', 'location', 'condition']

# Similarly, you can create forms for Employee, AssetAssignment, UsageHistory, and Maintenance
