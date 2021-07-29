from django.contrib.auth.tokens import default_token_generator
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from users.models import User
from users.serializers import UserSerializer
from users.utils import send_activation_link


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('users:user_list', request=request, format=format),
    })


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request)
        email = request.data.get('email', '')
        user = User.objects.get(email=email)
        if user:
            token = default_token_generator.make_token(user)
            activation_link = 'activate/?user_id={}&token={}'.format(
                              user.id, token)
            url = request.build_absolute_uri(activation_link)
            send_activation_link(request, user, url)
        else:
            print('You need to provide a valid email address.')
        return response

    @action(detail=False, methods=['GET'])
    def activate(self, request):
        user_id = request.query_params.get('user_id', '')
        confirmation_token = request.query_params.get('token', '')
        try:
            user = self.get_queryset().get(pk=user_id)
        except(TypeError, ValueError,  User.DoesNotExist):
            user = None
        if user is None:
            return Response('User not found',
                            status=status.HTTP_400_BAD_REQUEST)
        if not default_token_generator.check_token(user, confirmation_token):
            return Response('''Token is invalid or expired.
            Please request another confirmation email by signing in.''',
                            status=status.HTTP_400_BAD_REQUEST)
        user.is_active = True
        user.save()
        return Response('Email successfully confirmed')
