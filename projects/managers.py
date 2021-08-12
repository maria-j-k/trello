from django.db import models
from django.utils import timezone


class IssueManager(models.Manager):
    def has_overdue(self):
        return super().get_queryset().exclude(status=4).filter(
                due_date__lte=timezone.now().date())
