from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^addToList', views.addToList, name="addToList"),
    url(r'^addToMyList/(?P<id>\d*)$', views.addToMyList, name="addToMyList"),
    url(r'^viewUser/(?P<user_id>\d*)$', views.viewUser, name="viewUser"),
    url(r'^deleteList/(?P<id>\d*)$', views.deleteList, name="deleteList")
]