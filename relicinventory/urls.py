from django.urls import path

from . import views

app_name = "relicinventory"
urlpatterns = [
	path('my-inventory/', views.my_inventory, name="my-inventory"),

	#ajax views
	path('save-inventory-changes/', views.ajax_save_inventory_changes, name="save-changes")
]
