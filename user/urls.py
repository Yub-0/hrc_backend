from django.urls import path, re_path

from user import views
from user.views import UserLoginAPIView

urlpatterns = [
    path('login/', UserLoginAPIView.as_view(), name='login_user'),
    path('owner/', views.OwnerView.as_view()),
    path('', views.UserView.as_view()),
    re_path(r'(?P<pk>[0-9]+)', views.UserView.as_view())
]