from django.shortcuts import render
from django.http import  HttpResponse
import  requests

from .models import Theme, Category, Question, Answer
from core.models import HouseHoldData, OwnerFamilyData, OtherFamilyMember, AnimalDetailData

def calculateScore(request, id):
    this_house = HouseHoldData.objects.filter(index=id)
    mappable_questions = Question.objects.filter(directly_mappable=True)
    non_mappable_questions = Question.objects.filter(directly_mappable=False).values_list('map_to_model', 'map_to_field')
    for question in mappable_questions:
        final_score = 0
        level0_score = 0
        level1_score = 0
        level2_score = 0
        print(question, "==============")

    html = "<html><body><p>Ranking Households</p></body></html>"
    return HttpResponse(html)


# def calculateLevel0Score():
