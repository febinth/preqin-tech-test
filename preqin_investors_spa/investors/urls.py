from django.urls import path
from . import views

urlpatterns = [
    path('investors/', views.get_investors),
    path('investors/<int:investor_id>/', views.get_investor_details, name='investor_details')
]