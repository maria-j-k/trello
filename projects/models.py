from django.conf import settings
from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE,
                              blank=True,
                              null=True)
    creation_date = models.DateTimeField(auto_now_add=True)
