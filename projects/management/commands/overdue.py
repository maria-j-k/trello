from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand

from projects.models import Issue


class Command(BaseCommand):
    help = 'Sends alert email messages if an issue has gone overdue'

    ALERT_SUBJECT = 'Trello-clone: Issue has an overdue'
    ALERT_BODY = '''Your issue "{issue}" has gone overdue!
 The due date is {due_date}, the overdue is {overdue}.'''
    DEADLINE_BODY = '''Your issue's "{issue}" deadline is today!'''

    def send_overdue_mail(self, issue):
        if issue.overdue() == 0:
            body = self.DEADLINE_BODY.format(issue=issue.title)
        else:
            overdue = f'{issue.overdue()} day' if issue.overdue == 1 else \
                    f'{issue.overdue()} days'
            body = self.ALERT_BODY.format(issue=issue.title,
                                          due_date=issue.due_date,
                                          overdue=overdue)
        send_mail(
            self.ALERT_SUBJECT,
            body,
            settings.MAIL_INFO,
            [issue.assignee.email],
            fail_silently=False,
            )

    def handle(self, *args, **kwargs):
        for issue in Issue.objects.has_overdue():
            self.send_overdue_mail(issue)
