from django.conf import settings
from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              related_name='owned_projects',
                              on_delete=models.PROTECT,
                              blank=True, null=True)
    coworkers = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                       related_name='co_projects',
                                       blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.id}: {self.name}'


class Issue(models.Model):
    TODO = 1
    IN_PROGRESS = 2
    REVIEW = 3
    DONE = 4
    STATUS_CHOICES = [
        (TODO, 'todo'),
        (IN_PROGRESS, 'in progress'),
        (REVIEW, 'review'),
        (DONE, 'done'),
    ]
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField()
    project = models.ForeignKey(Project,
                                related_name='issues',
                                on_delete=models.CASCADE,
                                blank=True, null=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              related_name='owned_issues',
                              on_delete=models.PROTECT,
                              blank=True, null=True)
    assignee = models.ForeignKey(settings.AUTH_USER_MODEL,
                                 related_name='issues',
                                 on_delete=models.DO_NOTHING,
                                 blank=True, null=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=TODO)

    def __str__(self):
        return f'{self.id}: {self.title}'
