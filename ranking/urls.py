from django.urls import  path

from  .views import calculateScore

urlpatterns = [
    path('calculate-score/<int:id>', calculateScore, name='calculate_score'),
]