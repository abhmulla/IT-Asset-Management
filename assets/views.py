from django.shortcuts import render

from django.shortcuts import render, get_object_or_404, redirect
from .models import Asset, AssetType
from .forms import AssetForm, AssetTypeForm

import nmap
from django.shortcuts import render, redirect
from .forms import NetworkScanForm
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
# Create your views here.
# assets/views.py


def asset_list(request):
    asset_types = AssetType.objects.all()
    return render(request, 'assets/asset_list.html', {'asset_types': asset_types})

def specific_assets(request, asset_type_id):
    assets = Asset.objects.filter(asset_type_id=asset_type_id)
    asset_type = get_object_or_404(AssetType, id=asset_type_id)
    return render(request, 'assets/specific_assets.html', {'assets': assets, 'asset_type': asset_type})

def asset_detail(request, asset_id):
    asset = get_object_or_404(Asset, id=asset_id)
    return render(request, 'assets/asset_detail.html', {'asset': asset})

def add_asset(request):
    if request.method == "POST":
        form = AssetForm(request.POST)
        if form.is_valid():
            # Check if a new asset type was provided
            new_asset_type = request.POST.get('new_asset_type')
            if new_asset_type:
                # Create and save the new asset type
                asset_type, created = AssetType.objects.get_or_create(name=new_asset_type)
                # Assign the new asset type to the asset
                form.instance.asset_type = asset_type
            form.save()
            return redirect('asset_list')
    else:
        form = AssetForm()
    return render(request, 'assets/asset_form.html', {'form': form})
def edit_asset(request, asset_id):
    asset = get_object_or_404(Asset, id=asset_id)
    if request.method == "POST":
        form = AssetForm(request.POST, instance=asset)
        if form.is_valid():
            form.save()
            return redirect('asset_detail', asset_id=asset.id)
    else:
        form = AssetForm(instance=asset)
    return render(request, 'assets/asset_form.html', {'form': form})

def network_scan(request):
    if request.method == "POST":
        form = NetworkScanForm(request.POST)
        if form.is_valid():
            ip_range = form.cleaned_data["ip_range"] #?
            scanner = nmap.PortScanner()
            scanner.scan(ip_range, arguments="-sn")
            devices = []
            for ip in scanner.all_hosts():
                device = {
                    "ip": ip,
                    "hostname": scanner[ip].hostname(),
                    "mac": scanner[ip]["addresses"].get("mac", "N/A"),
                    "vendor": scanner[ip]["vendor"].get(scanner[ip]["addresses"].get("mac", ""), "N/A")
                }
                devices.append(device)
            return render(request, "assets/scan_results.html", {"devices": devices})
    else:
        form = NetworkScanForm()
    return render(request, 'assets/network_scan.html', {'form': form})

def generate_report(request):
    # Create a response object and set the PDF headers
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="assets_report.pdf"'

    # Create a canvas object using ReportLab
    c = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    # Add a title to the PDF
    c.setFont("Helvetica-Bold", 16)
    c.drawString(30, height - 40, "Assets Report")

    # Set up table headers
    c.setFont("Helvetica-Bold", 12)
    y = height - 80
    c.drawString(30, y, "Name")
    c.drawString(130, y, "Type")
    c.drawString(230, y, "Specific Type")
    c.drawString(330, y, "Cost")
    c.drawString(430, y, "Units")
    c.drawString(530, y, "Total Value")

    # Reset font for table content
    c.setFont("Helvetica", 12)
    y -= 20

    total_value = 0

    # Fetch all assets and add their details to the PDF
    for asset in Asset.objects.all():
        total_asset_value = asset.cost * asset.units
        total_value += total_asset_value
        c.drawString(30, y, asset.name)
        c.drawString(130, y, asset.asset_type.name)
        c.drawString(230, y, asset.specific_type)
        c.drawString(330, y, f"${asset.cost:.2f}")
        c.drawString(430, y, str(asset.units))
        c.drawString(530, y, f"${total_asset_value:.2f}")
        y -= 20
        if y < 40:  # Add a new page if the content exceeds one page
            c.showPage()
            y = height - 40
            c.setFont("Helvetica", 12)

    # Add the total value at the bottom
    c.setFont("Helvetica-Bold", 12)
    c.drawString(430, y, "Total Value")
    c.drawString(530, y, f"${total_value:.2f}")

    # Finalize the PDF
    c.showPage()
    c.save()
    return response
