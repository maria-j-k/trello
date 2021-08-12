from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator


SUBJECT = 'Trello-clone: Activate you account'
BODY = '''Welcome to Trello-clone!
To activate your account, please click the link:
{path}'''


def send_activation_link(request, user):
    path = make_activation_url(request, user)
    send_mail(
        SUBJECT,
        BODY.format(path=path),
        settings.MAIL_INFO,
        [user.email],
        fail_silently=False,
        )


def make_activation_url(request, user):
    token = default_token_generator.make_token(user)
    activation_link = 'activate/?user_id={}&token={}'.format(
                      user.id, token)
    return request.build_absolute_uri(activation_link)

