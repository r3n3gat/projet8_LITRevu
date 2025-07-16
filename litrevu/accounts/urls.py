# litrevu/accounts/urls.py

from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/',       views.signup,         name='signup'),
    path('login/',        views.login_view.as_view(), name='login'),
    path('logout/',       views.logout_confirm, name='logout'),
    path('profile/',      views.profile,        name='profile'),
    path('profile/edit/', views.profile_edit,   name='profile_edit'),
]
