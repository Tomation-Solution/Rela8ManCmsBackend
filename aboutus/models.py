from django.db import models
from authentication.models import User
from cloudinary_storage.storage import (
    MediaCloudinaryStorage,
)

# Create your models here.


class AboutHistory(models.Model):
    writer = models.OneToOneField(to=User, on_delete=models.SET_NULL, null=True)
    main_image = models.ImageField(
        storage=MediaCloudinaryStorage(),
        upload_to="images/about/history/",
        blank=True,
        null=True,
        default=None,
    )
    history_image = models.ImageField(
        storage=MediaCloudinaryStorage(),
        upload_to="images/about/history/",
        blank=True,
        null=True,
        default=None,
    )
    mission_image = models.ImageField(
        storage=MediaCloudinaryStorage(),
        upload_to="images/about/history/",
        blank=True,
        null=True,
        default=None,
    )
    vision_image = models.ImageField(
        storage=MediaCloudinaryStorage(),
        upload_to="images/about/history/",
        blank=True,
        null=True,
        default=None,
    )
    history_paragraphs = models.TextField()
    core_values = models.TextField()
    vision = models.TextField()
    mission = models.TextField()
    objectives = models.TextField()
    extras = models.TextField()
    # USED JSO FIELDS SO I CAN STORE AN ARRAY
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"about history {self.id}"

    class Meta:
        ordering = ["-created_at"]


class AboutAdvocacy(models.Model):
    writer = models.OneToOneField(to=User, on_delete=models.SET_NULL, null=True)
    main_image = models.ImageField(
        storage=MediaCloudinaryStorage(),
        upload_to="images/about/advocacy/",
        blank=True,
        null=True,
        default=None,
    )
    main_achievements = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"about advocacy {self.id}"

    class Meta:
        ordering = ["-created_at"]


class AboutAffilliate(models.Model):
    writer = models.OneToOneField(to=User, on_delete=models.SET_NULL, null=True)
    main_image = models.ImageField(
        storage=MediaCloudinaryStorage(),
        upload_to="images/about/affilliate/",
        blank=True,
        null=True,
        default=None,
    )

    ops = models.TextField()
    international_partners = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"about affilliate {self.id}"

    class Meta:
        ordering = ["-created_at"]


class AboutHowWeWork(models.Model):
    writer = models.OneToOneField(to=User, on_delete=models.SET_NULL, null=True)
    main_image = models.ImageField(
        storage=MediaCloudinaryStorage(),
        upload_to="images/about/how-we-work/",
        blank=True,
        null=True,
        default=None,
    )

    how_we_work_header = models.TextField(blank=True, null=True)
    how_we_work = models.TextField(blank=True, null=True)
    how_we_work_details = models.TextField(blank=True, null=True)

    committees_header = models.TextField(blank=True, null=True)
    committees = models.TextField(blank=True, null=True)
    committee_details = models.TextField(blank=True, null=True)

    adhoc_header = models.TextField(blank=True, null=True)
    adhoc = models.TextField(blank=True, null=True)

    spvehicles_header = models.TextField(blank=True, null=True)
    spvehicles = models.TextField(blank=True, null=True)

    spgroups_header = models.TextField(blank=True, null=True)
    spgroups = models.TextField(blank=True, null=True)

    conduct_header = models.TextField(blank=True, null=True)
    conduct = models.TextField(blank=True, null=True)

    conduct_listing_header = models.TextField(blank=True, null=True)
    conduct_listing = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"about how we work {self.id}"

    class Meta:
        ordering = ["-created_at"]


class AboutWhereWeOperate(models.Model):
    writer = models.OneToOneField(to=User, on_delete=models.SET_NULL, null=True)
    main_image = models.ImageField(
        storage=MediaCloudinaryStorage(),
        upload_to="images/about/where-we-operate/",
        blank=True,
        null=True,
        default=None,
    )
    national_secretariat_header = models.TextField(blank=True, null=True)
    national_secretariat = models.TextField()
    coorprate_office_header = models.TextField(blank=True, null=True)
    coorprate_office = models.TextField()
    branch_text_header = models.TextField(blank=True, null=True)
    branch_text = models.TextField()

    def __str__(self) -> str:
        return f"about where we operate {self.id}"


class AboutWhereWeOperateOffice(models.Model):
    writer = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=300)
    email = models.JSONField()
    phone_no = models.JSONField()
    address = models.CharField(max_length=300)
    website = models.URLField()

    def __str__(self) -> str:
        return f"about operate office {self.id}"


class AboutWhereWeOperateBranch(models.Model):
    writer = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=300)
    manager_name = models.CharField(max_length=300)
    title = models.CharField(max_length=300)
    email = models.JSONField()
    address = models.CharField(max_length=300)

    def __str__(self) -> str:
        return f"about branch {self.id}"


class AboutContactUs(models.Model):
    name = models.CharField(max_length=300)
    phone_no = models.CharField(max_length=20)
    email = models.EmailField()
    subject = models.TextField()
    message = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"about contact {self.id}"

    class Meta:
        ordering = ["-created_at"]


class AboutOurExecutives(models.Model):
    executive_type = [
        ("EXECUTIVE", "EXECUTIVE"),
        ("BRANCH", "BRANCH"),
        ("SECTORAL", "SECTORAL"),
        ("SPECIAL_PURPOSE_VEHICLES", "SPECIAL_PURPOSE_VEHICLES"),
        ("SPECIAL_PURPOSE_GROUPS", "SPECIAL_PURPOSE_GROUPS"),
        ("LIFE_MEMBERS", "LIFE_MEMBERS"),
        ("ELECTED_MEMBERS", "ELECTED_MEMBERS"),
        ("STRATEGIC_MEMBERS", "STRATEGIC_MEMBERS"),
    ]

    writer = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(
        storage=MediaCloudinaryStorage(), default=None, blank=True, null=True
    )
    name = models.CharField(max_length=300)
    title = models.CharField(max_length=300, unique=True)
    extra_title1 = models.CharField(max_length=300, blank=True, null=True)
    extra_title2 = models.CharField(max_length=300, blank=True, null=True)
    order_position = models.PositiveIntegerField(null=False, default=1)
    type = models.CharField(max_length=100, choices=executive_type)
    tenor = models.CharField(max_length=100, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.order_position is None:
            # Set to max existing position + 1 if not provided
            max_position = AboutOurExecutives.objects.aggregate(
                models.Max("order_position")
            )["order_position__max"]
            self.order_position = (max_position or 0) + 1
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"our executives: {self.name}"

    class Meta:
        ordering = ["-created_at"]
