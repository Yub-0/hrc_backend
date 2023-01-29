from django.urls import path, re_path

from house import views

urlpatterns = [
    path('rooms', views.RoomView.as_view()),
    re_path(r'rooms/(?P<pk>[0-9]+)', views.RoomView.as_view()),
    path('', views.HouseView.as_view()),
    re_path(r'(?P<pk>[0-9]+)', views.HouseView.as_view())
]
