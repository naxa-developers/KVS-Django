from celery import shared_task
import csv
from django.core.management import call_command

from ranking.views import calculateHouseHoldScore

@shared_task()
def calcScoreFromCelery(id):
    try:
        calculateHouseHoldScore(id)
        print("Successfully calculated score for household {}".format(id))
    except Exception as e:
        print("{} error occured for household {} with  message {}".format(type(e), id, e))
        f = open("error_list.csv", 'a')
        outfileWriter = csv.writer(f, delimiter=',')
        outfileWriter.writerow([id, e])
        f.close()