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
