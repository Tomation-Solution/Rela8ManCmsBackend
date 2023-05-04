from django.contrib import admin
from structure import models

# Register your models here.
admin.site.register(models.MPDCL)
admin.site.register(models.MPDCLServices)
admin.site.register(models.MRC)
admin.site.register(models.MRCServices)
admin.site.register(models.SectoralGroup)