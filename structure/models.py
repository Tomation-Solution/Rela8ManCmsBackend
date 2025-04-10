from django.db import models
from authentication.models import User
from cloudinary_storage.storage import (
    MediaCloudinaryStorage,
)


# Create your models here.
class SectoralGroup(models.Model):
    writer = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True)
    header = models.CharField(max_length=300, blank=False)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(
        storage=MediaCloudinaryStorage(), default=None, blank=True, null=True
    )


class MRC(models.Model):
    writer = models.OneToOneField(to=User, on_delete=models.SET_NULL, null=True)
    who_we_are = models.TextField()
    objectives = models.TextField()
    objectives_card = models.JSONField()  # array {header, description}


class MRCServices(models.Model):
    writer = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=300, blank=False)
    description = models.TextField()
    items = models.JSONField(blank=True, null=True)
    small_text = models.CharField(max_length=300)


class MPDCL(models.Model):
    writer = models.OneToOneField(to=User, on_delete=models.SET_NULL, null=True)
    who_we_are = models.TextField()
    our_objectives_header = models.TextField()
    our_objectives_items = models.TextField()
    renewable_image = models.ImageField(
        storage=MediaCloudinaryStorage(), default=None, blank=True, null=True
    )
    renewable_desc = models.TextField()
    renewable_items = models.JSONField()  # array{header, description}


class MPDCLServices(models.Model):
    service_type = [
        ("POWER_FACILITATION", "POWER_FACILITATION"),
        ("RENEWABLE_ENERGY", "RENEWABLE_ENERGY"),
        ("OTHERS", "OTHERS"),
    ]
    writer = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True)
    type = models.CharField(choices=service_type, max_length=300)
    header = models.CharField(max_length=300)
    description = models.TextField()
    image = models.ImageField(
        storage=MediaCloudinaryStorage(), blank=True, null=True, default=None
    )
