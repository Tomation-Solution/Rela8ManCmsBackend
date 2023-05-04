from django.db import models
from authentication.models import User

# Create your models here.


class Training(models.Model):
    training_type_choices = [
        ("MRC", "MRC"),
        ("MPDCL", "MPDCL"),
        ("OTHERS", "OTHERS")
    ]

    writer = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(
        upload_to='images/trainings/', blank=True, null=True)
    name = models.CharField(max_length=300)
    training_type = models.CharField(
        blank=False, choices=training_type_choices, max_length=100)
    # THE GROUP OR SECTION THE TRAINING IS FOR
    group_type = models.CharField(max_length=300)
    location = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    is_paid = models.BooleanField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"trainings || {self.id}"

    class Meta:
        ordering = ["-created_at"]
