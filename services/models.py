from django.db import models
from authentication.models import User
import secrets
# Create your models here.


class AllServices(models.Model):
    writer = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True)
    serviceType = [
        ('CORE', 'CORE'),
        ('MRC', 'MRC'),
        ('MPDCL', "MPDCL"),
        ('OTHERS', 'OTHERS')
    ]

    image = models.ImageField(default=None, blank=True, null=True)
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
    message = models.TextField()
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"request service {self.id}"

    class Meta:
        ordering = ["-created_at"]


class SubscribeToNewsLetter(models.Model):
    ref = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"new letter subscriber {self.id}"

    class Meta:
        ordering = ["-created_at"]
