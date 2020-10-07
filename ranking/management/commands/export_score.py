from django.core.management.base import BaseCommand, CommandError
from celery import shared_task
import csv

from ranking.views import calculateHouseHoldScore
from core.models import HouseHoldData
from ranking.tasks import calcScoreFromCelery

class Command(BaseCommand):
    help = "Use this command to calculate the risk score of all the data of HouseHold model"

    def handle(self, *args, **options):
        all_household = HouseHoldData.objects.all().order_by('id')
        for household in all_household:
            f = open("score_list.csv", 'a')
            outfileWriter = csv.writer(f, delimiter=',')
            outfileWriter.writerow([household.id, household.owner_name, household.risk_score])
            f.close()
