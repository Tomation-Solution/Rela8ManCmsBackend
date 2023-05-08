from django.db import models
from authentication.models import User

# Create your models here.


class Gallery(models.Model):
    writer = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.name} || {self.id}"

    class Meta:
        ordering = ["-created_at"]


class GalleryItems(models.Model):
    gallery = models.ForeignKey(to=Gallery, on_delete=models.CASCADE)
    caption = models.CharField(max_length=300)
    image = models.ImageField(
        upload_to='images/gallery/', blank=False, null=False)

    def __str__(self) -> str:
        return f"gallery item || {self.id}"
