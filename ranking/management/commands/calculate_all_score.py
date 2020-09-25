from django.core.management.base import BaseCommand, CommandError
from celery import shared_task

from ranking.views import calculateHouseHoldScore
from core.models import HouseHoldData
from ranking.tasks import calcScoreFromCelery

class Command(BaseCommand):
    help = "Use this command to calculate the risk score of all the data of HouseHold model"

    def handle(self, *args, **options):
        all_household = HouseHoldData.objects.all()
        for household in all_household:
            calcScoreFromCelery.delay(household.id)