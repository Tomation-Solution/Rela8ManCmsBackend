from django.contrib import admin
from payments import models

# Register your models here.

admin.site.register(models.PublicationPayment)
admin.site.register(models.EventTrainingRegistration)
admin.site.register(models.Luncheon)
admin.site.register(models.MembersAGMRegistration)
admin.site.register(models.ExhibitorsAGMRegistration)
admin.site.register(models.ExhibitionBoot)
admin.site.register(models.OthersAGMRegistration)
admin.site.register(models.AGMInvitation)
admin.site.register(models.QuickRegistration)
