from django.urls import path, re_path

from rent import views

urlpatterns = [
    path('category', views.CategoryView.as_view()),
    re_path(r'category/(?P<pk>[0-9]+)', views.CategoryView.as_view())
]