from django.db import models

# Create your models here.
class Table(models.Model):
    name = models.CharField(max_length=256)
    available = models.BooleanField(default=True)
    occupied = models.BooleanField(default=True)

    def __str__(self):
        return self.name