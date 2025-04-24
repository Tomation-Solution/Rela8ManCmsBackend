from django.db import models
from authentication.models import User
from cloudinary_storage.storage import (
    MediaCloudinaryStorage,
)


# Create your models here.
class EventBanner(models.Model):
    banner_image = models.ImageField(
        storage=MediaCloudinaryStorage(), default=None, blank=True, null=True
    )

    def __str__(self) -> str:
        return f"Event banner {self.id}"


class Event(models.Model):
    writer = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(
        storage=MediaCloudinaryStorage(),
        upload_to="images/events/",
        blank=True,
        null=True,
    )
    name = models.CharField(max_length=300)
    # WHETHER IT IS AN ANNUAL GENERAL MEETING EVENT OR NOT
    is_agm = models.BooleanField(default=False)
    is_current_agm = models.BooleanField(default=False)
    # THE GROUP OR SECTION THE EVENT IS FOR
    group_type = models.CharField(max_length=300)
    location = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    is_paid = models.BooleanField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"event || {self.id}"

    class Meta:
        ordering = ["-created_at"]


from django.db import models
from cloudinary_storage.storage import MediaCloudinaryStorage


class EventAndMediaContent(models.Model):
    banner_image = models.ImageField(
        storage=MediaCloudinaryStorage(),
        upload_to="images/media_content/main/",
        blank=True,
        null=True,
    )

    main_image = models.ImageField(
        storage=MediaCloudinaryStorage(),
        upload_to="images/media_content/main/",
        blank=True,
        null=True,
    )

    # News
    news_image = models.ImageField(
        storage=MediaCloudinaryStorage(),
        upload_to="images/media_content/news/",
        blank=True,
        null=True,
    )
    news_title = models.CharField(max_length=300)
    news_description = models.TextField()
    news_link_text = models.CharField(max_length=300)

    # Publication
    publication_image = models.ImageField(
        storage=MediaCloudinaryStorage(),
        upload_to="images/media_content/publications/",
        blank=True,
        null=True,
    )
    publication_title = models.CharField(max_length=300)
    publication_description = models.TextField()
    publication_link_text = models.CharField(max_length=300)

    # Event
    event_image = models.ImageField(
        storage=MediaCloudinaryStorage(),
        upload_to="images/media_content/events/",
        blank=True,
        null=True,
    )
    event_title = models.CharField(max_length=300)
    event_description = models.TextField()
    event_link_text = models.CharField(max_length=300)

    # Report
    report_image = models.ImageField(
        storage=MediaCloudinaryStorage(),
        upload_to="images/media_content/reports/",
        blank=True,
        null=True,
    )
    report_title = models.CharField(max_length=300)
    report_description = models.TextField()
    report_link_text = models.CharField(max_length=300)

    # Gallery
    gallery_image = models.ImageField(
        storage=MediaCloudinaryStorage(),
        upload_to="images/media_content/gallery/",
        blank=True,
        null=True,
    )
    gallery_title = models.CharField(max_length=300)
    gallery_description = models.TextField()
    gallery_link_text = models.CharField(max_length=300)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Event & Media Content || {self.id}"

    class Meta:
        ordering = ["-created_at"]
