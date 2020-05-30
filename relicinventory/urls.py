from django.urls import path

from . import views

app_name = "relicinventory"
urlpatterns = [
	path('my-inventory/', views.my_inventory, name="my-inventory")
]
