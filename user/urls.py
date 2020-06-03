from django.urls import path

from . import views

app_name = "user"
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.log_user_out, name='logout'),
    path('profile/', views.profile, name = 'profile'),
    path('register/', views.register, name = 'register'),
    path('link-wf-acc', views.link_warframe_account, name='link_wf_acc')
]