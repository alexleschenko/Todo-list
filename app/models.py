from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Todo(models.Model):
    task = models.CharField(max_length=100)
    done = models.BooleanField(default=False)
