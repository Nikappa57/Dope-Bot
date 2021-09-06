
from django.urls import path

from accounts import views


urlpatterns = [
    path('register/', views.register_view, name='register_view'),
]