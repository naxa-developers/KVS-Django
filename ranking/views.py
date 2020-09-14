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
    # if this_house.risk_score > 0:
    #     print("Household", this_house, "-------->", this_house.risk_score)
    themes = Theme.objects.all()
    categories = Category.objects.all().order_by('parent_theme')
    questions = Question.objects.all().order_by('scoring_method')
    answers = Answer.objects.all()
    return render(request, 'index.html', {'house': this_house, 'categories': categories, 'themes': themes, 'questions': questions, 'answers': answers})


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
        # if theme.calculated_value > 0:
        # print("Theme", theme.name, "-------->", theme.calculated_value)


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
        # if category.calculated_value > 0:
        # print("Category", category.name,
        #       "-------->", category.calculated_value)


def calculateQuestionScore(request, id):
    this_house = HouseHoldData.objects.filter(index=id)
    all_questions = Question.objects.all()
    for question in all_questions:
        if question.scoring_method in ['substrings', 'keywords', 'multifield_substring']:
            sample_answer = Answer.objects.filter(parent_question=question)[0]
            if sample_answer.answer_types == 'with_blank_rows':
                blank_mapping = {
                    'involved_disaster_training_type': ['No']
                }
                calculateCriteriaScore(question, this_house, blank_mapping)
            else:
                calculateCriteriaScore(question, this_house)
        elif question.scoring_method == 'yes/no':
            sample_answer = Answer.objects.filter(parent_question=question)[0]
            if sample_answer.answer_types == 'substrings':
                yes_mapping = {
                    'status_of_family_member': ['Pregnant', 'Milk feeding baby', 'Breast feeding woman'],
                    'disability_type': ['People with disability Chronic illness', 'Chronic illness'],
                    'social_security_received': ['Yes'],
                    'age_group': ['less than 5 years'],
                    'hazard_type': ['Earthquake', 'Fire', 'Flood', 'Snake bite', 'Road accident',  'Animal attack',  'Epidemic', 'question',
                                    'Thunderstorm', 'Drought',  'Windstorm', 'Drought', 'हावाहुरी'],
                    'fire_extinguisher_in_house': ["Yes"],
                    'early_warning_system_installed_nearby': ['Yes'],
                    'evacuation_shelter_availability': ['Yes'],
                    'prepared_contingency_plan': ['Yes']
                }
                calculateCriteriaScore(question, this_house, yes_mapping)
            elif sample_answer.answer_types == 'keywords':
                calculateCriteriaScore(question, this_house)
        elif question.scoring_method == 'code_mapping':
            code_mapping = {'What is status of the household head?':
                            {
                                '1': 'Female Leadership',
                                '2': 'Senior Citizen Leadership',
                                '3': 'Children Leadership',
                                '4': 'Single Women Leadership',
                                '5': 'Disabled Member Leadership',
                                '6': 'Others',
                                'nan': 'Others',
                            },
                            'Time taken to reach Open Space?':
                            {
                                'Near in the house': 'Walking Distance',
                                '15-30 minutes': '15-30 minutes',
                                '30 minutes-1 hour': '30 minutes to 1 hour',
                                'more than hour': 'more than hour',
                                '': "Don't Know",
                                'nan': "Don't Know",
                                'Dont Know': "Don't Know"
                            },
                            'Disaster Information Medium?':
                            {
                                'Related body': 'Related Body/Radio/TV',
                                'Radio/T.V /Local people': 'Related Body/Radio/TV',
                                'Local people': 'Related Body/Radio/TV',
                                'Local people Radio/T.V': 'Related Body/Radio/TV',
                                'Local peopleNewspaper': 'Related Body/Radio/TV',
                                'Hoarding board   Local people': 'Related Body/Radio/TV',
                                'Radio/T.V': 'Related Body/Radio/TV',
                                'Local people Radio/T.V': 'Related Body/Radio/TV',
                                'Related body  Local people Radio/T.V': 'Related Body/Radio/TV',
                                'Local peopleNewspaper': 'Related Body/Radio/TV',
                                '': 'No',
                                'nan': 'No',
                            },
                            'Any Damages occured in the time of Flood':
                            {
                                'Death': 'Death Casualty',
                                'Injured': 'Injured Family Members',
                                'Minor damages in walls': 'House',
                                'House was flooded': 'House',
                                'Damage in roof': 'House',
                                'Damage in foundation': 'House',
                                'Furniture': 'Furniture',
                                'Land': 'Land',
                                'Livestock': 'Livestock',
                                'Crops': 'Crops',
                                'Food Stock': 'Food Stock',
                                'Machineries': 'Machineries',
                                '': 'No',
                                'nan': 'No',
                                'Multiple': 'Multiple'
                            }
                            }
            calculateCriteriaScore(question, this_house, code_mapping)
        elif question.scoring_method == 'composite_count':
            if question.question == "Household have Senior Citizen of 70 years?":
                check_phrases = ["Senior citizen of 70 years", ]
            elif question.question == "Dalit, Senior Citizen of 60 years?":
                check_phrases = ["Senior Citizen of 60 years", "Dalit"]
            elif question.question == "Unmarried 60 years old woman":
                check_phrases = ["Unmarried 60 years old woman"]
            elif question.question == "60 years old single woman":
                check_phrases = ["60 years old single woman"]
            elif question.question == "Widow of any age?":
                check_phrases = ["Widow of any age"]
            calculateCriteriaScore(question, this_house, check_phrases)


def calculateCriteriaScore(*args):
    this_question = args[0]
    # print(this_question, this_question.scoring_method)
    if this_question.scoring_method == 'substrings':
        map_to_field1 = this_question.map_to_field_1
        map_to_model = this_question.map_to_model
        sample_answer = Answer.objects.filter(parent_question=this_question)
        if sample_answer[0].answer_types == 'substrings':
            if map_to_model == "HouseHoldData":
                sample_answer = Answer.objects.filter(
                    parent_question=this_question)
                household_answer = args[1].values_list(
                    map_to_field1, flat=True)
                selected_answer = Answer.objects.annotate(answer_field=Value(household_answer[0], output_field=CharField(
                ))).filter(parent_question=this_question, answer_field__icontains=F('answer_choice'))
                this_score = selected_answer[0].weight * \
                    this_question.weight if len(selected_answer) > 0 else 0
                this_question.calculated_value = this_score
                this_question.save()
        elif sample_answer[0].answer_types == 'with_blank_rows':
            if map_to_model == "HouseHoldData":
                sample_answer = Answer.objects.filter(
                    parent_question=this_question)
                household_answer = args[1].values_list(
                    map_to_field1, flat=True)
                if household_answer[0] == '' or household_answer[0] == 'nan' or household_answer[0] == None:
                    selected_answer = Answer.objects.filter(
                        parent_question=this_question, answer_choice__in=args[2][map_to_field1])
                else:
                    selected_answer = Answer.objects.annotate(answer_field=Value(household_answer[0], output_field=CharField(
                    ))).filter(parent_question=this_question, answer_field__icontains=F('answer_choice'))
                this_score = selected_answer[0].weight * \
                    this_question.weight if len(selected_answer) > 0 else 0
                this_question.calculated_value = this_score
                this_question.save()

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
                        # print("Question ", this_question, "-------->",
                        #       this_question.calculated_value)

    elif this_question.scoring_method == "composite_count":
        map_to_field1 = this_question.map_to_field_1
        map_to_field2 = this_question.map_to_field_2
        map_to_model = this_question.map_to_model
        if map_to_model == "OwnerFamilyData":
            sample_answer = Answer.objects.filter(
                parent_question=this_question)
            if sample_answer[0].answer_types == 'substrings':
                check_phrases = args[2]
                owner_families = OwnerFamilyData.objects.filter(
                    parent_index=args[1][0].index).values_list(map_to_field1, flat=True)
                count = 0
                for member in owner_families:
                    for check_phrase in check_phrases:
                        if check_phrase in member:
                            count = count + 1
                if count > 1:
                    selected_answer = Answer.objects.filter(
                        answer_choice__icontains='More than 1')
                    this_score = selected_answer[0].weight * \
                        this_question.weight
                elif count == 1:
                    selected_answer = Answer.objects.filter(
                        answer_choice__icontains='1')
                    this_score = selected_answer[0].weight * \
                        this_question.weight
                else:
                    selected_answer = Answer.objects.filter(
                        answer_choice__icontains='No')
                    this_score = selected_answer[0].weight * \
                        this_question.weight
                this_question.calculated_value = this_score
                this_question.save()
                # print("Question ", this_question, "-------->",
                #         this_question.calculated_value)

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
                possible_answers = args[2][this_question.map_to_field_1]
                for member in owner_families:
                    if member[0] in possible_answers:
                        keyword = "Yes"
                selected_answer = Answer.objects.filter(
                    parent_question=this_question, answer_choice=keyword)
                this_score = selected_answer[0].weight * \
                    this_question.weight
                this_question.calculated_value = this_score
                this_question.save()
                # print("Question ", this_question, "--------->",
                #       this_question.calculated_value)
        elif map_to_model == "HouseHoldData":
            sample_answer = Answer.objects.filter(
                parent_question=this_question)
            if sample_answer[0].answer_types == 'substrings':
                keyword = 'No'
                possible_answers = args[2][this_question.map_to_field_1]
                household_answer = args[1].values_list(
                    map_to_field1, flat=True)
                if household_answer[0] in possible_answers:
                    keyword = 'Yes'
                selected_answer = Answer.objects.filter(
                    parent_question=this_question, answer_choice__icontains=keyword)
                this_score = selected_answer[0].weight * \
                    this_question.weight
                this_question.calculated_value = this_score
                this_question.save()
                # print("Question ", this_question, "--------->",
                #       this_question.calculated_value)
            elif sample_answer[0].answer_types == 'keywords':
                household_answer = args[1].values_list(
                    map_to_field1, flat=True)
                keyword = 'No'
                if household_answer[0] == 'Yes':
                    keyword = household_answer[0]
                selected_answer = Answer.objects.filter(
                    parent_question=this_question, answer_choice=keyword)
                this_score = selected_answer[0].weight * \
                    this_question.weight
                this_question.calculated_value = this_score
                this_question.save()
                # print("Question ", this_question, "--------->",
                #       this_question.calculated_value)

    elif this_question.scoring_method == "code_mapping":
        map_to_field1 = this_question.map_to_field_1
        map_to_model = this_question.map_to_model
        if map_to_model == "HouseHoldData":
            sample_answer = Answer.objects.filter(
                parent_question=this_question)
            if sample_answer[0].answer_types == 'code_mapping':
                household_answer = args[1].values_list(
                    map_to_field1, flat=True)
                this_owner_answer = args[2][str(
                    this_question.question)][household_answer[0].strip()]
                selected_answer = Answer.objects.filter(
                    parent_question=this_question, answer_choice__icontains=this_owner_answer)
                this_score = selected_answer[0].weight * \
                    this_question.weight if len(selected_answer) > 0 else 0
                this_question.calculated_value = this_score
                this_question.save()
                # print("Question ", this_question, "--------->",
                #       this_question.calculated_value)
            elif sample_answer[0].answer_types == 'substrings':
                this_owner_answer = []
                household_answer = args[1].values_list(
                    map_to_field1, flat=True)
                for answer in args[2][this_question.question]:
                    if household_answer[0].strip() in answer:
                        this_owner_answer.append(
                            args[2][this_question.question][answer])
                if len(this_owner_answer) > 1:
                    selected_answer = Answer.objects.filter(
                        parent_question=this_question, answer_choice__icontains='Multiple')
                else:
                    selected_answer = Answer.objects.filter(
                        parent_question=this_question, answer_choice__icontains=this_owner_answer[0])
                this_score = selected_answer[0].weight * \
                    this_question.weight if len(selected_answer) > 0 else 0
                this_question.calculated_value = this_score
                this_question.save()

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
                # print("Question ", this_question, "--------->",
                #       this_question.calculated_value)
        if sample_answer[0].answer_types == 'substrings':
            if map_to_model == "HouseHoldData":
                household_answer = args[1].values_list(
                    map_to_field1, flat=True)
                selected_answer = Answer.objects.filter(
                    parent_question=this_question, answer_choice__iexact=household_answer[0])
                this_score = selected_answer[0].weight * \
                    this_question.weight
                this_question.calculated_value = this_score
                this_question.save()
                # print("Question ", this_question, "--------->",
                #       this_question.calculated_value)
