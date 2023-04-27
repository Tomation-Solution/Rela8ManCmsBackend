from django.db import models
from authentication.models import User
# Create your models here.


class AboutHistory(models.Model):
    writer = models.OneToOneField(
        to=User, on_delete=models.SET_NULL, null=True)
    main_image = models.ImageField(
        upload_to='images/about/history/', blank=True, null=True, default=None)
    history_image = models.ImageField(
        upload_to='images/about/history/', blank=True, null=True, default=None)
    mission_image = models.ImageField(
        upload_to='images/about/history/', blank=True, null=True, default=None)
    vision_image = models.ImageField(
        upload_to='images/about/history/', blank=True, null=True, default=None)
    # USED JSO FIELDS SO I CAN STORE AN ARRAY
    history_paragraphs = models.JSONField()
    core_values = models.JSONField()
    vision = models.JSONField()
    mission = models.JSONField()
    objectives = models.JSONField()
    extras = models.JSONField()
    # USED JSO FIELDS SO I CAN STORE AN ARRAY
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"about history {self.id}"

    class Meta:
        ordering = ["-created_at"]


class AboutAdvocacy(models.Model):
    writer = models.OneToOneField(
        to=User, on_delete=models.SET_NULL, null=True)
    main_image = models.ImageField(
        upload_to='images/about/advocacy/', blank=True, null=True, default=None)
    # USED JSO FIELDS SO I CAN STORE AN ARRAY
    main_achievements = models.JSONField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"about advocacy {self.id}"

    class Meta:
        ordering = ["-created_at"]


class AboutAffilliate(models.Model):
    writer = models.OneToOneField(
        to=User, on_delete=models.SET_NULL, null=True)
    main_image = models.ImageField(
        upload_to='images/about/affilliate/', blank=True, null=True, default=None)
    # USED JSO FIELDS SO I CAN STORE AN ARRAY
    ops = models.JSONField()
    international_partners = models.JSONField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"about affilliate {self.id}"

    class Meta:
        ordering = ["-created_at"]


class AboutHowWeWork(models.Model):
    writer = models.OneToOneField(
        to=User, on_delete=models.SET_NULL, null=True)
    main_image = models.ImageField(
        upload_to='images/about/how-we-work/', blank=True, null=True, default=None)
    # USED JSO FIELDS SO I CAN STORE AN ARRAY
    how_we_work = models.JSONField()
    how_we_work_details = models.JSONField()
    committees = models.JSONField()
    committee_details = models.JSONField()
    adhoc = models.JSONField()
    spvehicles = models.JSONField()
    spgroups = models.JSONField()
    conduct = models.JSONField()
    conduct_listing = models.JSONField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"about how we work {self.id}"

    class Meta:
        ordering = ["-created_at"]


class AboutWhereWeOperate(models.Model):
    writer = models.OneToOneField(
        to=User, on_delete=models.SET_NULL, null=True)
    main_image = models.ImageField(
        upload_to='images/about/where-we-operate/', blank=True, null=True, default=None)
    national_secretariat = models.TextField()
    coorprate_office = models.TextField()
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
        ("STRATEGIC_MEMBERS", "STRATEGIC_MEMBERS")
    ]

    writer = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(default=None, blank=True, null=True)
    name = models.CharField(max_length=300)
    title = models.CharField(max_length=300)
    extra_title1 = models.CharField(max_length=300, blank=True, null=True)
    extra_title2 = models.CharField(max_length=300, blank=True, null=True)
    type = models.CharField(max_length=100, choices=executive_type)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"our executives: {self.name}"

    class Meta:
        ordering = ["-created_at"]
