from django.db import models


class HomePageSlider(models.Model):
    title = models.CharField(max_length=200)
    content= models.TextField()
    banner = models.ImageField()

    def __str__(self):
        return self.title