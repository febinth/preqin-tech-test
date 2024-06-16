from django.urls import path
from . import views

urlpatterns = [
    path('investors/', views.get_investors),
]