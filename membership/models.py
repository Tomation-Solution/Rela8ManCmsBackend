from django.db import models
from authentication.models import User
# Create your models here.


class WhyJoinMan(models.Model):
    whyjoin = [
        ("REASONS", "REASONS"),
        ("OTHERS", "OTHERS"),
    ]
    writer = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True)
    header = models.CharField(max_length=300)
    description = models.TextField()
    type = models.CharField(choices=whyjoin, max_length=300)

    def __str__(self) -> str:
        return f"Why join MAN: {self.id}"


class JoiningStep(models.Model):
    writer = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True)
    step_name = models.CharField(max_length=300)
    step_list = models.JSONField(blank=True, null=False)
    step_description = models.TextField(blank=True, null=False, default="")
    step_extras = models.JSONField(blank=True, null=False)

    def __str__(self) -> str:
        return f"Steps to join MAN: {self.id}"


class FAQs(models.Model):
    writer = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True)
    header = models.CharField(max_length=400)
    content = models.JSONField()

    def __str__(self) -> str:
        return f"FAQ: {self.id}"


class HomePage(models.Model):
    writer = models.OneToOneField(
        to=User, on_delete=models.SET_NULL, null=True)
    Logo = models.ImageField(blank=True, null=True, default=None)
    slider_welcome_message = models.CharField(max_length=255)
    slider_vision_message = models.CharField(max_length=255)
    slider_mission_message = models.CharField(max_length=255)

    vision_intro = models.JSONField()
    mission_intro = models.JSONField()
    advocacy_intro = models.JSONField()
    history_intro = models.JSONField()
    why_join_intro = models.JSONField()
    members_intro = models.JSONField()

    slider_image1 = models.ImageField(blank=True, null=True, default=None)
    slider_image2 = models.ImageField(blank=True, null=True, default=None)
    slider_image3 = models.ImageField(blank=True, null=True, default=None)

    def __str__(self) -> str:
        return f"Home page main: {self.id}"


class WhyWeAreUnique(models.Model):
    writer = models.ForeignKey(
        to=User, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(default=None, blank=True, null=True)
    heading = models.CharField(max_length=300)
    description = models.TextField()

    def __str__(self) -> str:
        return f"why we are unique {self.id}"


class OurMembers(models.Model):
    writer = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=300)
    website = models.URLField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"our members {self.id}"

    class Meta:
        ordering = ["-created_at"]
