from django.db.models import Value, F, CharField
from django.shortcuts import render
from django.http import HttpResponse
import requests

from .models import Theme, Category, Question, Answer
from core.models import HouseHoldData, OwnerFamilyData, OtherFamilyMember, AnimalDetailData


def calculateHouseHoldScore(request, id):
    calculateThemeScore(request, id)
    this_house = HouseHoldData.objects.get(index=id)
    all_themes = Theme.objects.all()
    this_household_score = 0
    for theme in all_themes:
        this_household_score = this_household_score + \
            theme.calculated_value if theme.calculated_value != None else this_household_score
    this_house.risk_score = this_household_score
    this_house.save()
    if this_house.risk_score > 0:
        print("Household", this_house, "-------->", this_house.risk_score)
    themes = Theme.objects.all()
    categories = Category.objects.all()
    questions = Question.objects.all()
    answers = Answer.objects.all()
    return render(request, 'index.html', {'house': this_house, 'categories': categories, 'themes': themes, 'questions':questions, 'answers': answers})


def calculateThemeScore(request, id):
    calculateCategoryScore(request, id)
    all_themes = Theme.objects.all()
    for theme in all_themes:
        theme_categories = Category.objects.filter(parent_theme=theme)
        this_theme_score = 0
        for th in theme_categories:
            this_theme_score = this_theme_score + \
                th.calculated_value if th.calculated_value != None else this_theme_score
        theme.calculated_value = this_theme_score
        theme.save()
        if theme.calculated_value > 0:
            print("Theme", theme.name, "-------->", theme.calculated_value)


def calculateCategoryScore(request, id):
    calculateQuestionScore(request, id)
    all_categories = Category.objects.all()
    for category in all_categories:
        category_questions = Question.objects.filter(parent_category=category)
        this_category_score = 0
        for qn in category_questions:
            this_category_score = this_category_score + \
                qn.calculated_value if qn.calculated_value != None else this_category_score
        category.calculated_value = this_category_score
        category.save()
        if category.calculated_value > 0:
            print("Category", category.name,
                  "-------->", category.calculated_value)


def calculateQuestionScore(request, id):
    this_house = HouseHoldData.objects.filter(index=id)
    all_questions = Question.objects.all()
    for question in all_questions:
        if question.scoring_method in ['substrings', 'keywords', 'composite_count', 'multifield_substring']:
            calculateCriteriaScore(question, this_house)
        elif question.scoring_method == 'yes/no':
            if question.map_to_field_1 == 'status_of_family_member':
                yes_mapping = ['Pregnant', 'Milk feeding baby',
                               'Breast feeding woman']
            elif question.map_to_field_1 == 'disability_type':
                yes_mapping = [
                    'People with disability Chronic illness', 'Chronic illness']
            elif question.map_to_field_1 == 'social_security_received':
                yes_mapping = ['Yes']
            elif question.map_to_field_1 == 'age_group':
                yes_mapping = ['less than 5 years']
            calculateCriteriaScore(question, this_house, yes_mapping)
        elif question.scoring_method == 'code_mapping':
            code_mapping = {1: 'Female Leadership',
                            2: 'Senior Citizen Leadership',
                            3: 'Children Leadership',
                            4: 'Single Women Leadership',
                            5: 'Disabled Member Leadership',
                            6: 'Others'}
            calculateCriteriaScore(question, this_house, code_mapping)


def calculateCriteriaScore(*args):
    this_question = args[0]
    # print(this_question, this_question.scoring_method)
    if this_question.scoring_method == 'substrings':
        map_to_field1 = this_question.map_to_field_1
        map_to_model = this_question.map_to_model
        if map_to_model == "HouseHoldData":
            sample_answer = Answer.objects.filter(
                parent_question=this_question)
            if sample_answer[0].answer_types == 'substrings':
                household_answer = args[1].values_list(
                    map_to_field1, flat=True)
                selected_answer = Answer.objects.annotate(answer_field=Value(household_answer[0], output_field=CharField(
                ))).filter(parent_question=this_question, answer_field__icontains=F('answer_choice'))
                this_score = selected_answer[0].weight * this_question.weight if len(selected_answer)>0 else 0
                this_question.calculated_value = this_score
                this_question.save()
                print("Question ", this_question, "------->",
                      this_question.calculated_value)
                # answers = Answer.objects.filter(parent_question=this_question)
                # for answer in answers:
                #     print(answer.answer_choice, household_answer[0])
                #     if answer.answer_choice in household_answer[0]:
                #         selected_answer = answer
                #     else:
                #         selected_answer = ''
                #     print(selected_answer)
    elif this_question.scoring_method == "multifield_substring":
        map_to_field1 = this_question.map_to_field_1
        map_to_field2 = this_question.map_to_field_2
        map_to_model = this_question.map_to_model
        if map_to_model == "OwnerFamilyData":
            sample_answer = Answer.objects.filter(
                parent_question=this_question)
            if sample_answer[0].answer_types == 'complex_calculation':
                owner_families = OwnerFamilyData.objects.filter(
                    parent_index=args[1][0].index).values_list('status_of_family_member', 'disability_type')
                for member in owner_families:
                    if member[0] == "People with disability":
                        selected_answer = Answer.objects.annotate(disability_type=Value(member[1], output_field=CharField(
                        ))).filter(parent_question=this_question, disability_type__icontains=F('answer_choice'))
                        if selected_answer.count() > 1:
                            this_score = 1 * this_question.weight
                        else:
                            this_score = selected_answer[0].weight * \
                                this_question.weight
                        this_question.calculated_value = this_score
                        this_question.save()
                        print("Question ", this_question, "-------->",
                              this_question.calculated_value)

    elif this_question.scoring_method == "yes/no":
        map_to_field1 = this_question.map_to_field_1
        map_to_model = this_question.map_to_model
        if map_to_model == "OwnerFamilyData":
            sample_answer = Answer.objects.filter(
                parent_question=this_question)
            if sample_answer[0].answer_types == 'substrings':
                owner_families = OwnerFamilyData.objects.filter(
                    parent_index=args[1][0].index).values_list(this_question.map_to_field_1)
                keyword = 'No'
                for member in owner_families:
                    if member[0] in args[2]:
                        keyword = "Yes"
                selected_answer = Answer.objects.filter(
                    parent_question=this_question, answer_choice=keyword)
                this_score = selected_answer[0].weight * \
                    this_question.weight
                this_question.calculated_value = this_score
                this_question.save()
                print("Question ", this_question, "--------->",
                      this_question.calculated_value)
    elif this_question.scoring_method == "code_mapping":
        # print(this_question, this_question.scoring_method)
        map_to_field1 = this_question.map_to_field_1
        map_to_model = this_question.map_to_model
        if map_to_model == "HouseHoldData":
            sample_answer = Answer.objects.filter(
                parent_question=this_question)
            if sample_answer[0].answer_types == 'substrings':
                household_answer = args[1].values_list(
                    map_to_field1, flat=True)
                selected_answer = Answer.objects.annotate(answer_field=Value(household_answer[0], output_field=CharField(
                ))).filter(parent_question=this_question, answer_field__icontains=F('answer_choice'))
                this_owner_answer = args[2][int(household_answer[0])]
                selected_answer = Answer.objects.filter(
                    parent_question=this_question, answer_choice__icontains=this_owner_answer)
                this_score = selected_answer[0].weight * \
                    this_question.weight
                this_question.calculated_value = this_score
                this_question.save()
                print("Question ", this_question, "--------->",
                      this_question.calculated_value)
    elif this_question.scoring_method == "keywords":
        map_to_field1 = this_question.map_to_field_1
        map_to_model = this_question.map_to_model
        sample_answer = Answer.objects.filter(
            parent_question=this_question)
        if sample_answer[0].answer_types == 'keywords':
            if map_to_model == "HouseHoldData":
                household_answer = args[1].values_list(
                    map_to_field1, flat=True)
                selected_answer = Answer.objects.filter(
                    parent_question=this_question, answer_choice__iexact=household_answer[0])
                this_score = selected_answer[0].weight * \
                    this_question.weight
                this_question.calculated_value = this_score
                this_question.save()
                print("Question ", this_question, "--------->",
                      this_question.calculated_value)
