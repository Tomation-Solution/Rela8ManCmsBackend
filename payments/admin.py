from django.contrib import admin
from payments import models

# Register your models here.

admin.site.register(models.PublicationPayment)
admin.site.register(models.EventTrainingRegistration)
admin.site.register(models.AGMRegistration)
