from django.db import models
from cloudinary_storage.storage import RawMediaCloudinaryStorage


class AGMHomepageCMS(models.Model):
    main_image = models.ImageField(
        upload_to="images/agm/", blank=True, null=True)
    intro_text = models.TextField()
    location = models.TextField()

    agm_start_date = models.DateField()
    countdown_text = models.CharField(max_length=300)

    intro_title = models.CharField(max_length=500)
    intro_description = models.TextField()

    exhibition_text = models.CharField(max_length=300)
    exhibition_image = models.ImageField(
        upload_to="images/agm/", blank=True, null=True)

    save_date_text = models.CharField(max_length=300)
    save_date_image = models.ImageField(
        upload_to="images/agm/", blank=True, null=True)

    venue_text = models.CharField(max_length=300)
    venue_text_image = models.ImageField(
        upload_to="images/agm/", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "AGM homepage cms"
        verbose_name_plural = "AGM homepage cms"


class AGMProgrammeCMS(models.Model):
    main_image = models.ImageField(
        upload_to="images/agm/", blank=True, null=True)
    main_text = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "AGM programme cms"
        verbose_name_plural = "AGM programme cms"


class AGMPrograms(models.Model):
    program_date = models.DateField()
    program_title = models.CharField(unique=True)
    program_attached_file_link = models.URLField(blank=True, null=True)
    program_attached_file1 = models.FileField(
        storage=RawMediaCloudinaryStorage, blank=True, null=True)
    program_attached_file2 = models.FileField(
        storage=RawMediaCloudinaryStorage, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "AGM Program"
        verbose_name_plural = "AGM Programs"
        ordering = ["created_at"]


class AGMSpeakers(models.Model):
    intro_text = models.CharField(max_length=300)
    header = models.CharField(max_length=300)
    speaker_title = models.CharField(max_length=300, blank=True, null=True)
    speaker_name = models.CharField(max_length=300)
    extra_title = models.CharField(max_length=300, blank=True, null=True)
    speaker_image = models.ImageField(
        upload_to="images/agm/", blank=True, null=True)
    speaker_words = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "AGM Speaker"
        verbose_name_plural = "AGM Speakers"


class AGMVenue(models.Model):
    venue_image = models.ImageField(
        upload_to="images/agm/", blank=True, null=True)
    venue_location_text = models.TextField()
    venue_location_map = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "AGM Venue"
        verbose_name_plural = "AGM Venues"


class AGMExhibitionCMS(models.Model):
    main_image = models.ImageField(
        upload_to="images/agm/", blank=True, null=True)
    intro_text = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "AGM exhibition cms"
        verbose_name_plural = "AGM exhibition cms"


class AGMPreviousExhibitionAndCompanyImages(models.Model):
    image_type = [
        ("exhibition", "exhibition"),
        ("company", "company")
    ]

    image = models.ImageField(upload_to="images/agm/", blank=True, null=True)
    type = models.CharField(max_length=100, choices=image_type)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "AGM previouse exhibition and company image"
        verbose_name_plural = "AGM previous exhibition and company images"


class AGMFAQ(models.Model):
    header = models.CharField(max_length=400)
    content = models.TextField()

    class Meta:
        verbose_name = "AGM Faq"
        verbose_name_plural = "AGM Faqs"
