from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from rest_framework.reverse import reverse


SUBJECT = 'Trello-clone: Issue assignement'
ASSAIGNEMENT_BODY = '''You've been assigned to the issue {issue}.
 Go to the issue: {path}'''
REVOCATION_BODY = '''You've been revoked form the issue {issue}.'''
ALERT_SUBJECT = 'Trello-clone: Issue has an overdue'
ALERT_BODY = '''Your issue {issue} has gone overdue! The due date is {due_date},
the overdue is {overdue}. To see your task, go to {path}'''
DEADLINE_BODY = '''Your issue's {issue} deadline is today!
 To see your tsk, to to {path}'''


def send_assaignement_link(request, user, issue):
    path = reverse('projects:issue-detail',
                   kwargs={'project_pk': issue.project.pk, 'pk': issue.pk},
                   request=request)
    send_mail(
        SUBJECT,
        ASSAIGNEMENT_BODY.format(issue=issue.title, path=path),
        settings.MAIL_INFO,
        [user.email],
        fail_silently=False,
        )


def send_revocation_link(request, user, issue):
    path = reverse('projects:issue-detail',
                   kwargs={'project_pk': issue.project.pk, 'pk': issue.pk},
                   request=request)
    send_mail(
        SUBJECT,
        REVOCATION_BODY.format(issue=issue.title, path=path),
        settings.MAIL_INFO,
        [user.email],
        fail_silently=False,
        )


def send_info_mails(request, issue, previous=None):
    if previous:
        send_revocation_link(request, previous, issue)
    send_assaignement_link(request, issue.assignee, issue)
    return None


def send_overdue_mail(request, issue):
    path = reverse('projects:issue-detail',
                   kwargs={'project_pk': issue.project.pk, 'pk': issue.pk},
                   request=request)
    diff = timezone.now().date() - issue.due_date
    if diff.days() == 0:
        body = DEADLINE_BODY.format(issue=issue.title, path=path)
    else:
        overdue = f'{diff} day' if diff == 1 else f'{diff} days'
        body = ALERT_BODY.format(issue=issue.title,
                                 due_date=issue.due_date,
                                 overdue=overdue,
                                 path=path),
    send_mail(
        ALERT_SUBJECT,
        body,
        settings.MAIL_INFO,
        [issue.assignee.email],
        fail_silently=False,
        )
