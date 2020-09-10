from django.urls import  path

from  .views import calculateHouseHoldScore

urlpatterns = [
    path('calculate-score/<int:id>', calculateHouseHoldScore, name='calculate_score'),
]