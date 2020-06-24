from django.urls import path

from . import views

app_name = "user"
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.log_user_out, name='logout'),
    path('profile/', views.profile, name = 'profile'),
    path('register/', views.register, name = 'register'),
    path('link-wf-acc', views.link_warframe_account, name='link_wf_acc'),
    path('cant-log-in', views.cant_log_in, name='cant_log_in'),
    path('linked-wf-acc-req', views.linked_warframe_account_required, name='linked_wfa_required'),
    path('test-email-verification-msg/', views.test_send_email_verification_msg, name="test_email_verif_msg")#TODO: REMOVE THIS PATH!
]