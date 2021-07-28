from django.urls import path

from users import views


app_name = 'users'

user_list = views.UserViewSet.as_view({
    'post': 'create',
    'get': 'list'
    })
user_activate = views.UserViewSet.as_view({
    'get': 'activate'
    })

urlpatterns = [
    path('', user_list, name='user_list'),
    path('activate/', user_activate, name='user_activate')
    ]
