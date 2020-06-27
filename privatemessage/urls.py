from django.urls import path

from . import views

app_name = "privatemessage"
urlpatterns = [
    path('', views.index, name='index'),
	path('manager', views.manager, name="manager"),
]