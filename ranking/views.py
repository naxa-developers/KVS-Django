from django.shortcuts import render
from django.http import  HttpResponse
import  requests

from .models import Theme, Category, Question, Answer
from core.models import HouseHoldData, OwnerFamilyData, OtherFamilyMember, AnimalDetailData

def calculateScore(request, id):
    this_house = HouseHoldData.objects.filter(index=id)
    mappable_questions = Question.objects.filter(directly_mappable=True)
    non_mappable_questions = Question.objects.filter(directly_mappable=False)
    for question in mappable_questions:
        final_score = 0
        level0_score = 0
        level1_score = 0
        level2_score = 0
        print(question, "==============")
    # all_fields = HouseHoldData._meta.fields
    all_fields = [f.name for f in HouseHoldData._meta.get_fields()]
    print(all_fields)
    html = "<html><body><p>Ranking Households</p></body></html>"
    return HttpResponse(html)


# def calculateLevel0Score():
