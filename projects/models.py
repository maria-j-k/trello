from django.conf import settings
from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              related_name='owned_projects',
                              on_delete=models.CASCADE,
                              blank=True, null=True)
    coworkers = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                       related_name='co_projects',
                                       blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
