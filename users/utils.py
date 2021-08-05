from django.core.mail import send_mail
from django.conf import settings


SUBJECT = 'Trello-clone: Activate you account'
BODY = '''Welcome to Trello-clone!
To activate your account, please click the link:
{path}'''


def send_activation_link(request, user, path):
    send_mail(
        SUBJECT,
        BODY.format(path=path),
        settings.MAIL_INFO,
        [user.email],
        fail_silently=False,
        )
