from django.urls import  re_path

from tenant.views import TenantView

urlpatterns = [
    re_path(r'(?P<pk>[0-9]+)', TenantView.as_view()),
    re_path(r'', TenantView.as_view())
]
