from django.urls import  path

from  .views import calc

urlpatterns = [
    path('calculate-score/<int:id>', calc, name='calculate_score'),
]