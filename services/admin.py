from django.contrib import admin
from services.models import AllServices, SubscribeToNewsLetter, RequestService

# Register your models here.
admin.site.register(RequestService)
admin.site.register(SubscribeToNewsLetter)
admin.site.register(AllServices)
