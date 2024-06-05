# assets/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.asset_list, name='asset_list'),
    path('assets/<int:asset_type_id>/', views.specific_assets, name='specific_assets'),
    path('asset/<int:asset_id>/', views.asset_detail, name='asset_detail'),
    path('asset/add/', views.add_asset, name='add_asset'),
    path('asset/edit/<int:asset_id>/', views.edit_asset, name='edit_asset'),
    path('network_scan/', views.network_scan, name='network_scan'),
    path('generate_report/', views.generate_report, name='generate_report'),
    #path('network_scan/scan_results/', views.a, name="scan_results"),
]
