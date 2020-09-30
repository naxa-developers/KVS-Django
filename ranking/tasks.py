from celery import shared_task
from django.core.management import call_command

from ranking.views import calculateHouseHoldScore

@shared_task()
def calcScoreFromCelery(id):
    try:
        calculateHouseHoldScore(id)
        print("Successfully calculated score for household {}".format(id))
    except Exception as e:
        print("{} error occured for household {} with  message {}".format(type(e), id, e))
