import logging
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import serializers, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from users.models import User
from users.serializers import UserSerializer
from users.utils import send_activation_link


logger = logging.getLogger(__name__)


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('users:user_list', request=request, format=format),
    })


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            headers = self.get_success_headers(serializer.data)
            token = default_token_generator.make_token(user)
            activation_link = 'activate/?user_id={}&token={}'.format(
                              user.id, token)
            url = request.build_absolute_uri(activation_link)
            send_activation_link(request, user, url)
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED,
                            headers=headers)
        else:
            logger.error('Somebody has entered an invalid email!')
            return Response('You need to provide a valid email address',
                            status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['GET'])
    def activate(self, request):
        user_id = request.query_params.get('user_id', '')
        user_id = serializers.IntegerField().to_internal_value(data=user_id) 
        confirmation_token = request.query_params.get('token', '')
        user = get_object_or_404(self.get_queryset(), pk=user_id)
        if not default_token_generator.check_token(user, confirmation_token):
            return Response('''Token is invalid or expired.
            Please request another confirmation email by signing in.''',
                            status=status.HTTP_400_BAD_REQUEST)
        user.is_active = True
        user.save()
        return Response('Email successfully confirmed',
                        status=status.HTTP_200_OK)
