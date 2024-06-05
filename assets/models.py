from django.db import models

# Create your models here.

class AssetType(models.Model):
    name = models.CharField(max_length=13, default="AssetType")
    description = models.TextField(blank=True)
    def __str__(self):
        return self.name

class Asset(models.Model):
    ASSET_STATUS = (
        ("available", "Available"),
        ("maintenance", "Maintenance"),
        ("borrowed", "Borrowed")
    )
    asset_type = models.ForeignKey(AssetType, related_name= "assets", on_delete=models.CASCADE)
    specific_type = models.CharField(max_length=15)
    status = models.CharField(max_length=50, choices=ASSET_STATUS)
    notes = models.TextField(blank=True)
    name = models.CharField(max_length=100, default="Asset")
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    units = models.DecimalField(max_digits=10, decimal_places=0, default=1)

    def __str__(self):
        return f"{self.specific_type} ({self.asset_type.name})"