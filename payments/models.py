import uuid
from django.utils import timezone
from django.db import models
from publications.models import Publication
from events.models import Event
from trainings.models import Training
from authentication.models import User

# Create your models here.


class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ("paystack", "Paystack"),
        ("flutterwave", "Flutterwave"),
        ("remita", "Remita"),
        ("interswitch", "Interswitch"),
    ]

    payment_ref = models.CharField(max_length=300, unique=True, null=True, blank=True)
    amount = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    payment_method = models.CharField(
        max_length=50, choices=PAYMENT_METHOD_CHOICES, null=True, blank=True
    )
    access_code = models.CharField(max_length=300, blank=True, null=True)
    status = models.CharField(
        max_length=100,
        choices=[
            ("pending", "Pending"),
            ("success", "Success"),
            ("failed", "Failed"),
        ],
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment {self.payment_ref} - {self.payment_method}"


class PaymentDetail(models.Model):
    payment = models.OneToOneField(Payment, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=255)
    additional_info = models.JSONField()

    def __str__(self):
        return f"Payment Detail for {self.payment.payment_ref}"


class PublicationPayment(models.Model):
    payment = models.ForeignKey(
        Payment,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="payments",
    )
    publication = models.ForeignKey(Publication, on_delete=models.SET_NULL, null=True)
    fullname = models.CharField(max_length=300, blank=False)
    email = models.EmailField(blank=False)
    phone_number = models.CharField(blank=False, max_length=20)
    company_name = models.CharField(max_length=300, blank=False)
    amount_to_pay = models.DecimalField(max_digits=20, decimal_places=2)
    is_verified = models.BooleanField(default=False)
    file_received = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Publication Purchase {self.email}"

    class Meta:
        ordering = ["-created_at"]


class EventTrainingRegistration(models.Model):
    type_of_registration = [
        ("EVENT", "EVENT"),
        ("TRAINING", "TRAINING"),
    ]

    payment = models.ForeignKey(
        Payment, on_delete=models.SET_NULL, null=True, blank=True
    )
    fullname = models.CharField(max_length=300, blank=False)
    email = models.EmailField(blank=False)
    phone_number = models.CharField(blank=False, max_length=20)
    company_name = models.CharField(max_length=300, blank=False)
    event_type = models.CharField(
        max_length=100, choices=type_of_registration, blank=False
    )
    training = models.ForeignKey(
        to=Training, on_delete=models.SET_NULL, null=True, blank=True
    )
    event = models.ForeignKey(
        to=Event, on_delete=models.SET_NULL, null=True, blank=True
    )
    amount_to_pay = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Training or Event Registration {self.id}"

    class Meta:
        ordering = ["-created_at"]


class Luncheon(models.Model):
    luncheon_types = [("member", "member"), ("exhibitor", "exhibitor")]
    type = models.CharField(max_length=100, choices=luncheon_types, unique=True)
    price = models.DecimalField(max_digits=20, decimal_places=2, default=10000.00)


class MembersAGMRegistration(models.Model):
    payment = models.ForeignKey(
        Payment, on_delete=models.SET_NULL, null=True, blank=True
    )
    email = models.EmailField(blank=False)
    company_name = models.CharField(max_length=300)
    company_address = models.CharField(max_length=300)
    participant = models.JSONField()
    is_verified = models.BooleanField(default=False)
    mail_recevied = models.BooleanField(default=False)
    amount_to_pay = models.DecimalField(
        max_digits=20, decimal_places=2
    )  # luncheon price
    event = models.ForeignKey(
        to=Event, on_delete=models.SET_NULL, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"members AGM registration {self.id}"

    class Meta:
        ordering = ["-created_at"]


class ExhibitorsAGMRegistration(models.Model):
    payment = models.ForeignKey(
        Payment, on_delete=models.SET_NULL, null=True, blank=True
    )
    email = models.EmailField(blank=False)
    company_name = models.CharField(max_length=300)
    company_address = models.CharField(max_length=300)
    participant = models.JSONField()
    amount_to_pay = models.DecimalField(
        max_digits=20, decimal_places=2, default=0.00
    )  # luncheon price
    luncheon_covered_participants = models.IntegerField(default=0)
    boot = models.JSONField()
    is_verified = models.BooleanField(default=False)
    mail_recevied = models.BooleanField(default=False)
    event = models.ForeignKey(
        to=Event, on_delete=models.SET_NULL, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"AGM Registration {self.id}"

    class Meta:
        ordering = ["-created_at"]


class ExhibitionBoot(models.Model):
    writer = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    name = models.CharField(max_length=200)
    is_occupied = models.BooleanField(default=False)
    rented_by = models.ForeignKey(
        to=ExhibitorsAGMRegistration, on_delete=models.SET_NULL, null=True, blank=True
    )


class OthersAGMRegistration(models.Model):
    type_choices = [
        ("exhibitor-participant", "exhibitor-participant"),
        ("guest", "guest"),
        ("media", "media"),
        ("staff", "staff"),
    ]

    payment = models.ForeignKey(
        Payment, on_delete=models.SET_NULL, null=True, blank=True
    )
    type = models.CharField(max_length=200, choices=type_choices)
    company_name = models.CharField(max_length=300)
    designation = models.CharField(max_length=300)
    name = models.CharField(max_length=300)
    email = models.EmailField(blank=False)
    phone_no = models.CharField(max_length=50)
    event = models.ForeignKey(
        to=Event, on_delete=models.SET_NULL, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"AGM Registration Others {self.id}"

    class Meta:
        ordering = ["-created_at"]


class AGMInvitation(models.Model):
    type_choices = [
        ("guest", "guest"),
        ("media", "media"),
        ("staff", "staff"),
    ]

    type = models.CharField(max_length=200, choices=type_choices)
    company_name = models.CharField(max_length=300)
    email = models.EmailField()
    is_valid = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class QuickRegistration(models.Model):
    company_name = models.CharField(max_length=300)
    designation = models.CharField(max_length=300)
    name = models.CharField(max_length=300)
    email = models.EmailField(blank=False)
    phone_no = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"AGM Quick Registration {self.id}"

    class Meta:
        ordering = ["-created_at"]


class PublicationDownloadLink(models.Model):
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    publication_payment = models.ForeignKey(
        "PublicationPayment", on_delete=models.CASCADE
    )
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return timezone.now() > self.expires_at

    def __str__(self):
        return f"Download link for {self.publication_payment.email} (expires {self.expires_at})"
