from datetime import datetime
from django.db import models


class Photo(models.Model):
    name = models.CharField(max_length=200)
    picture = models.ImageField(upload_to='photos/', null=True, blank=True)
    date = models.DateTimeField(default=datetime.now, blank=True)