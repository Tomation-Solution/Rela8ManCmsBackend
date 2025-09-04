from django.db import models
from cloudinary_storage.storage import (
    MediaCloudinaryStorage,
)


class HomePageSlider(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    banner = models.ImageField(
        storage=MediaCloudinaryStorage(),
        null=True,
        upload_to="sliderbanner/%Y/",
        default=None,
    )
    order_position = models.PositiveIntegerField(null=True)
    is_archived = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.order_position is None:
            # Set to max existing position + 1 if not provided
            max_position = HomePageSlider.objects.aggregate(
                models.Max("order_position")
            )["order_position__max"]
            self.order_position = (max_position or 0) + 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class FooterContent(models.Model):
    logo = models.ImageField(
        storage=MediaCloudinaryStorage(),
        null=True,
        blank=True,
        upload_to="footer/%Y/",
        default=None,
    )
    company_name = models.CharField(max_length=200, default="")
    address = models.TextField(default="")
    email = models.EmailField(default="")
    phone = models.CharField(max_length=100, default="")
    webmail_url = models.URLField(blank=True, default="")
    branch_network_url = models.CharField(max_length=200, blank=True, default="")
    services_url = models.CharField(max_length=200, blank=True, default="")

    # Social Media URLs
    facebook_url = models.URLField(blank=True, default="")
    linkedin_url = models.URLField(blank=True, default="")
    twitter_url = models.URLField(blank=True, default="")
    instagram_url = models.URLField(blank=True, default="")
    youtube_url = models.URLField(blank=True, default="")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Footer Content"
        verbose_name_plural = "Footer Content"

    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        if not self.pk and FooterContent.objects.exists():
            # If this is a new instance and one already exists, update the existing one
            existing = FooterContent.objects.first()
            self.pk = existing.pk
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Footer Content - {self.company_name}"

    @classmethod
    def get_instance(cls):
        """Get the single footer content instance, create if doesn't exist"""
        instance, created = cls.objects.get_or_create(
            pk=1,  # Force primary key to be 1
            defaults={
                "company_name": "Your Company Name",
                "address": "Your Company Address",
                "email": "info@yourcompany.com",
                "phone": "+1234567890",
            },
        )
        return instance
