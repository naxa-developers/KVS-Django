from celery import shared_task
from django.core.management import call_command

from ranking.views import calculateHouseHoldScore

@shared_task()
def calcScoreFromCelery(id):
    calculateHouseHoldScore(id)