from django.urls import path
from . import views

urlpatterns = [
    path('', views.root),
    path('signin',views.signin),
    path('registration', views.registration),
    path('login', views.login),
    path('logout',views.logout),
    path('patients/',views.patients),
    path('account',views.account),
    path('payments/',views.payments),
    path('appointment_validate', views.appointment_validate),
]