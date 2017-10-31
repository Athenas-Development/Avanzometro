from django.conf.urls import url
from apps.login.views import index

urlpatterns = [
    url(r'^$', index),
]
