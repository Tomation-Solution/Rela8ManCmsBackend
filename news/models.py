from django.db import models

# Create your models here.
from django.db import models
from authentication.models import User
from cloudinary_storage.storage import RawMediaCloudinaryStorage
# Create your models here.


class News(models.Model):
    writer = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(
        upload_to='images/news/', blank=True, null=True, default=None)
    name = models.CharField(max_length=300)
    title = models.CharField(max_length=300)
    details = models.JSONField()
    link = models.FileField(upload_to='documents/news/%d/', null=True, default=None,
                            storage=RawMediaCloudinaryStorage())
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.id} || {str(self.writer)}"

    class Meta:
        ordering = ["-created_at"]
