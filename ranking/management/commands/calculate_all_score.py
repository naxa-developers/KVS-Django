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
        f = open("score_list.csv", 'a')
        f.truncate(0)
        for household in all_household:
            try:
                score = calculateHouseHoldScore(household.id)
                print("Successfully calculated score for household {} is {}".format(household.id, score[0]))
                outfileWriter = csv.writer(f, delimiter=',')
                outfileWriter.writerow([household.id, household.owner_name, score[1][0], score[1][1], score[1][2], score[1][3], score[0]])
            except Exception as e:
                print("{} error occured for household {} with  message {}".format(type(e), household.id, e))
                f = open("error_list.csv", 'a')
                outfileWriter = csv.writer(f, delimiter=',')
                outfileWriter.writerow([household.id, e])
