from django.contrib import admin
from publications import models

# Register your models here.
admin.site.register(models.Publication)
admin.site.register(models.PublicationParagraph)
