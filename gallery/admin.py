from django.contrib import admin
from gallery import models
# Register your models here.

admin.site.register(models.Gallery)
admin.site.register(models.GalleryItems)
