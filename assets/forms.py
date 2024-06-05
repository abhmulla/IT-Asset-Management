# assets/forms.py

from django import forms
from .models import Asset, AssetType
from django import forms
from . models import Asset, AssetType
class AssetTypeForm(forms.ModelForm):
    class Meta:
        model = AssetType
        fields = ['name', 'description']

class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['name', 'asset_type', 'specific_type', 'cost', 'units', 'status', 'notes']

class NetworkScanForm(forms.Form):
    ip_range = forms.CharField(label='IP Range', max_length=100, help_text="Enter IP range in CIDR format (e.g., 192.168.1.0/24)")



