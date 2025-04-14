from django.db import models
from django.contrib.postgres.fields import ArrayField

class Assessment(models.Model):
    title = models.CharField(max_length=255)
    link = models.URLField()
    description =  models.TextField(null=True, blank=True)
    remote_support = models.BooleanField(default=False)
    adaptive_support = models.BooleanField(default=False)
    test_type = models.JSONField()  # stores list of letters like ["A", "E", "B"]
    duration_min = models.PositiveIntegerField(null=True, blank=True)
    embedding = ArrayField(models.FloatField(), null=True, blank=True) 

    def __str__(self):
        return self.title
