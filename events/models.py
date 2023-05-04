from django.db import models
from authentication.models import User
# Create your models here.


class Event(models.Model):
    writer = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(
        upload_to='images/events/', blank=True, null=True)
    name = models.CharField(max_length=300)
    # WHETHER IT IS AN ANNUAL GENERAL MEETING EVENT OR NOT
    is_agm = models.BooleanField(default=False)
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
