from django.db import models

from publications.models import Publication
from events.models import Event
from trainings.models import Training

# Create your models here.


class PublicationPayment(models.Model):
    ref = models.CharField(max_length=300)
    fullname = models.CharField(max_length=300, blank=False)
    email = models.EmailField(blank=False)
    phone_number = models.CharField(blank=False, max_length=20)
    company_name = models.CharField(max_length=300, blank=False)
    publication = models.ForeignKey(
        to=Publication, on_delete=models.SET_NULL, null=True)
    amount_to_pay = models.DecimalField(max_digits=10, decimal_places=2)
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

    ref = models.CharField(max_length=300)
    fullname = models.CharField(max_length=300, blank=False)
    email = models.EmailField(blank=False)
    phone_number = models.CharField(blank=False, max_length=20)
    company_name = models.CharField(max_length=300, blank=False)
    type = models.CharField(
        max_length=100, choices=type_of_registration, blank=False)
    training = models.ForeignKey(
        to=Training, on_delete=models.SET_NULL, null=True, blank=True)
    event = models.ForeignKey(
        to=Event, on_delete=models.SET_NULL, null=True, blank=True)
    amount_to_pay = models.DecimalField(max_digits=10, decimal_places=2)
    is_verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"Training or Event Registration {self.id}"

    class Meta:
        ordering = ["-created_at"]


class AGMRegistration(models.Model):
    ref = models.CharField(max_length=300)
    email = models.EmailField(blank=False)
    company_name = models.CharField(max_length=300)
    company_address = models.CharField(max_length=300)
    participant_details = models.JSONField()
    is_verified = models.BooleanField(default=False)
    amount_to_pay = models.DecimalField(max_digits=10, decimal_places=2)
    event = models.ForeignKey(
        to=Event, on_delete=models.SET_NULL, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"AGM Registration {self.id}"

    class Meta:
        ordering = ["-created_at"]
