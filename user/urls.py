from django.urls import path, re_path

from user import views
from user.views import UserLoginAPIView

urlpatterns = [
    path('login/', UserLoginAPIView.as_view(), name='login_user'),
    path('', views.UserView.as_view()),
    re_path(r'(?P<pk>[0-9]+)', views.UserView.as_view())
]