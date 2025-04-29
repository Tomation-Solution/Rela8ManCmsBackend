from django.db import models
from cloudinary_storage.storage import RawMediaCloudinaryStorage, MediaCloudinaryStorage
from events.models import Event
from django.db.models import Q, UniqueConstraint


class AGMHomepageCMS(models.Model):
    event_id = models.OneToOneField(
        Event, on_delete=models.CASCADE, null=True, blank=True
    )
    main_image = models.ImageField(
        storage=MediaCloudinaryStorage(), upload_to="images/agm/", blank=True, null=True
    )
    intro_text = models.TextField(blank=True, null=True)
    location = models.TextField(blank=True, null=True)

    agm_start_date = models.DateField(blank=True, null=True)
    countdown_text = models.CharField(max_length=300, blank=True, null=True)

    intro_title = models.CharField(max_length=500, blank=True, null=True)
    intro_description = models.TextField(blank=True, null=True)

    exhibition_text = models.CharField(max_length=300, blank=True, null=True)
    exhibition_image = models.ImageField(
        storage=MediaCloudinaryStorage(), upload_to="images/agm/", blank=True, null=True
    )

    save_date_text = models.CharField(max_length=300, blank=True, null=True)
    save_date_image = models.ImageField(
        storage=MediaCloudinaryStorage(), upload_to="images/agm/", blank=True, null=True
    )

    venue_text = models.CharField(max_length=300, blank=True, null=True)
    venue_text_image = models.ImageField(
        storage=MediaCloudinaryStorage(), upload_to="images/agm/", blank=True, null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "AGM homepage cms"
        verbose_name_plural = "AGM homepage cms"


class AGMProgrammeCMS(models.Model):
    event_id = models.OneToOneField(
        Event, on_delete=models.CASCADE, null=True, blank=True
    )
    main_image = models.ImageField(
        storage=MediaCloudinaryStorage(), upload_to="images/agm/", blank=True, null=True
    )
    main_text = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "AGM programme cms"
        verbose_name_plural = "AGM programme cms"


class AGMPrograms(models.Model):
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
    program_date = models.DateField(blank=True, null=True)
    program_title = models.CharField(max_length=500, blank=True, null=True)
    program_attached_file_link = models.URLField(blank=True, null=True)
    program_attached_file1 = models.FileField(
        storage=RawMediaCloudinaryStorage, blank=True, null=True
    )
    program_attached_file2 = models.FileField(
        storage=RawMediaCloudinaryStorage, blank=True, null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "AGM Program"
        verbose_name_plural = "AGM Programs"
        ordering = ["created_at"]

        constraints = [
            # enforce uniqueness of program_title within an event, but only when program_title is not null or empty
            UniqueConstraint(
                fields=["event_id", "program_title"],
                condition=Q(program_title__isnull=False) & ~Q(program_title=""),
                name="unique_program_title_per_event_when_nonempty",
            )
        ]


class AGMSpeakers(models.Model):
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
    intro_text = models.CharField(max_length=300, blank=True, null=True)
    header = models.CharField(max_length=300, blank=True, null=True)
    speaker_title = models.CharField(max_length=300, blank=True, null=True)
    speaker_name = models.CharField(max_length=300, blank=True, null=True)
    extra_title = models.CharField(max_length=300, blank=True, null=True)
    speaker_image = models.ImageField(
        storage=MediaCloudinaryStorage(), upload_to="images/agm/", blank=True, null=True
    )
    speaker_words = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "AGM Speaker"
        verbose_name_plural = "AGM Speakers"


class AGMVenue(models.Model):
    event_id = models.OneToOneField(
        Event, on_delete=models.CASCADE, null=True, blank=True
    )
    venue_image = models.ImageField(
        storage=MediaCloudinaryStorage(), upload_to="images/agm/", blank=True, null=True
    )
    venue_location_text = models.TextField(blank=True, null=True)
    venue_location_map = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "AGM Venue"
        verbose_name_plural = "AGM Venues"


class AGMExhibitionCMS(models.Model):
    event_id = models.OneToOneField(
        Event, on_delete=models.CASCADE, null=True, blank=True
    )
    main_image = models.ImageField(
        storage=MediaCloudinaryStorage(), upload_to="images/agm/", blank=True, null=True
    )
    intro_text = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "AGM exhibition cms"
        verbose_name_plural = "AGM exhibition cms"


class AGMPreviousExhibitionAndCompanyImages(models.Model):
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
    image_type = [("exhibition", "exhibition"), ("company", "company")]

    image = models.ImageField(
        storage=MediaCloudinaryStorage(), upload_to="images/agm/", blank=True, null=True
    )
    type = models.CharField(max_length=100, choices=image_type, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "AGM previouse exhibition and company image"
        verbose_name_plural = "AGM previous exhibition and company images"


class AGMFAQ(models.Model):
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
    header = models.CharField(max_length=400, blank=True, null=True)
    content = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "AGM Faq"
        verbose_name_plural = "AGM Faqs"
