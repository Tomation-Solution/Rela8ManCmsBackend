from django.contrib import admin
from services.models import (
    AllServices,
    SubscribeToNewsLetter,
    RequestService,
    NewsletterUIConfig,
)

# Register your models here.
admin.site.register(RequestService)
admin.site.register(SubscribeToNewsLetter)
admin.site.register(AllServices)


@admin.register(NewsletterUIConfig)
class NewsletterUIConfigAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # Limit to only one entry
        return not NewsletterUIConfig.objects.exists() or super().has_add_permission(
            request
        )

    def has_delete_permission(self, request, obj=None):
        return True  # Prevent deletion
