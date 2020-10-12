from django.core.management.base import BaseCommand, CommandError
from celery import shared_task
import csv
import time

from ranking.views import calculateHouseHoldScore
from core.models import HouseHoldData
from ranking.tasks import calcScoreFromCelery

class Command(BaseCommand):
    help = "Use this command to calculate the risk score of all the data of HouseHold model"

    def handle(self, *args, **options):
        all_household = HouseHoldData.objects.all().order_by('id')
        for household in all_household:
            try:
                score = calculateHouseHoldScore(household.id)
                print("Successfully calculated score for household {} is {}".format(household.id, score))
            except Exception as e:
                print("{} error occured for household {} with  message {}".format(type(e), household.id, e))
                f = open("error_list.csv", 'a')
                outfileWriter = csv.writer(f, delimiter=',')
                outfileWriter.writerow([household.id, e])
                f.close()
