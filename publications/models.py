from django.db import models
from authentication.models import User
from cloudinary_storage.storage import RawMediaCloudinaryStorage
# Create your models here.


class PublicationType(models.Model):
    writer = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=300, blank=False)

    def __str__(self) -> str:
        return f"Type of publication {self.id}"


class Publication(models.Model):
    writer = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(
        upload_to='images/publications/', blank=True, null=True, default=None)
    name = models.CharField(max_length=300)
    title = models.CharField(max_length=300)
    link = models.FileField(upload_to='documents/publications/', null=True, default=None,
                            storage=RawMediaCloudinaryStorage())
    details = models.JSONField()
    is_paid = models.BooleanField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    type = models.ForeignKey(
        to=PublicationType, on_delete=models.SET_NULL, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.id} || {str(self.writer)}"

    class Meta:
        ordering = ["-created_at"]
