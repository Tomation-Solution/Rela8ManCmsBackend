from django.db import models
from authentication.models import User
from cloudinary_storage.storage import (
    RawMediaCloudinaryStorage,
    MediaCloudinaryStorage,
)

# Create your models here.


class Reports(models.Model):
    writer = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(
        storage=MediaCloudinaryStorage(),
        upload_to="images/reports/",
        blank=True,
        null=True,
        default=None,
    )
    name = models.CharField(max_length=300)
    report_content = models.TextField()  # Changed from details to report_content
    link = models.FileField(
        upload_to="documents/reports/%d/",
        null=True,
        blank=True,
        default=None,
        storage=RawMediaCloudinaryStorage(),
    )
    readmore_link = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.id} || {self.name} || {str(self.writer)}"

    class Meta:
        ordering = ["-created_at"]
