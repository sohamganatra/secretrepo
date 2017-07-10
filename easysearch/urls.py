from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.EasySearch),
    url(r'^results/$', views.SearchResults),
]
