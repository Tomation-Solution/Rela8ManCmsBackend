from django.db import models
from authentication.models import User
import secrets
from cloudinary_storage.storage import (
    MediaCloudinaryStorage,
)

# Create your models here.


class ServiceBanner(models.Model):
    banner_image = models.ImageField(
        storage=MediaCloudinaryStorage(), default=None, blank=True, null=True
    )
    mrc_desc = models.TextField()
    mpdcl_desc = models.TextField()
    core_desc = models.TextField()

    def __str__(self) -> str:
        return f"Service banner {self.id}"


class AllServices(models.Model):
    writer = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True)
    serviceType = [
        ("CORE", "CORE"),
        ("MRC", "MRC"),
        ("MPDCL", "MPDCL"),
        ("OTHERS", "OTHERS"),
    ]

    image = models.ImageField(
        storage=MediaCloudinaryStorage(), default=None, blank=True, null=True
    )
    name = models.CharField(max_length=300)
    description = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=300, choices=serviceType)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"Service {self.id}"

    class Meta:
        ordering = ["-created_at"]


class RequestService(models.Model):
    ref = models.CharField(max_length=100)
    name = models.CharField(max_length=300)
    email = models.EmailField()
    company_name = models.CharField(max_length=300)
    type = models.TextField(null=True, blank=True, help_text="Type of service request")
    service = models.TextField(null=True, blank=True)
    message = models.TextField()
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"request service {self.id}"

    class Meta:
        ordering = ["-created_at"]


class SubscribeToNewsLetter(models.Model):
    name = models.CharField(max_length=255)
    ref = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"Newsletter Subscriber: {self.name} ({self.email})"

    class Meta:
        ordering = ["-created_at"]


class NewsletterUIConfig(models.Model):
    header = models.CharField(max_length=255)
    description = models.TextField()
    btn_text = models.CharField(max_length=100)
    form_image = models.ImageField(
        storage=MediaCloudinaryStorage(),
        upload_to="images/newsletter_ui/",
        blank=True,
        null=True,
        default=None,
    )

    def __str__(self):
        return "Newsletter UI Configuration"

    class Meta:
        verbose_name = "Newsletter UI Configuration"
        verbose_name_plural = "Newsletter UI Configuration"
