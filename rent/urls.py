from django.urls import path, re_path

from rent import views

urlpatterns = [
    path('category', views.CategoryView.as_view()),
    re_path(r'category/(?P<pk>[0-9]+)', views.CategoryView.as_view()),
    path('payment', views.PaymentView.as_view()),
    re_path(r'payment/(?P<pk>[0-9]+)', views.PaymentView.as_view()),
    path('', views.RentView.as_view()),
    re_path(r'(?P<pk>[0-9]+)', views.RentView.as_view())
]