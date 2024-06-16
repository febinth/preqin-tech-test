from django.urls import path
from . import views

urlpatterns = [
    path('investors/', views.get_investors),
    path('investors/<int:investor_id>/', views.get_investor_details, name='investor_details'),
    path('investor/commitment/<str:asset_class>/<int:investor_id>/', views.get_commitments, name='commitment_details')
]