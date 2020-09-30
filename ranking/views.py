from django.db.models import Value, F, CharField
from django.shortcuts import render
from django.http import HttpResponse
import requests
from celery import shared_task

from .models import Theme, Category, Question, Answer
from core.models import HouseHoldData, OwnerFamilyData, OtherFamilyMember, AnimalDetailData
from .utils import flatten, returnNum, splitIntStr


def calc(request, id):
    from .tasks import calcScoreFromCelery
    this_household_score = calculateHouseHoldScore(id)
    these_houses = HouseHoldData.objects.filter(id=id)
    for house in these_houses:
        this_house = house
    themes = Theme.objects.all()
    categories = Category.objects.all().order_by('parent_theme')
    questions = Question.objects.all().order_by('parent_category')
    answers = Answer.objects.all()
    return render(request, 'index.html', {'house': this_house, 'categories': categories, 'themes': themes, 'questions': questions, 'answers': answers})


def calculateHouseHoldScore(id):
    calculateThemeScore(id)
    these_houses = HouseHoldData.objects.filter(id=id)
    for house in these_houses:
        this_house = house
        all_themes = Theme.objects.all()
        this_household_score = 0
        for theme in all_themes:
            this_household_score = this_household_score + \
                theme.calculated_value if theme.calculated_value != None else this_household_score
        this_house.risk_score = this_household_score
        this_house.save()
        themes = Theme.objects.all()
        categories = Category.objects.all().order_by('parent_theme')
        questions = Question.objects.all().order_by('parent_category')
        answers = Answer.objects.all()
        return this_household_score


def calculateThemeScore(id):
    calculateCategoryScore(id)
    all_themes = Theme.objects.all()
    for theme in all_themes:
        theme_categories = Category.objects.filter(parent_theme=theme)
        this_theme_score = 0
        for th in theme_categories:
            this_theme_score = this_theme_score + \
                th.calculated_value if th.calculated_value != None else this_theme_score
        theme.calculated_value = this_theme_score
        theme.save()


def calculateCategoryScore(id):
    calculateQuestionScore(id)
    all_categories = Category.objects.all()
    for category in all_categories:
        category_questions = Question.objects.filter(parent_category=category)
        this_category_score = 0
        for qn in category_questions:
            this_category_score = this_category_score + \
                qn.calculated_value if qn.calculated_value != None else this_category_score
        category.calculated_value = this_category_score
        category.save()


def calculateQuestionScore(id):
    this_house = HouseHoldData.objects.filter(index=id)
    all_questions = Question.objects.all()
    for question in all_questions:
        if question.scoring_method in ['substrings', 'keywords', 'multifield_substring', 'range_based']:
            sample_answer = Answer.objects.filter(parent_question=question)[0]
            if sample_answer.answer_types == 'with_blank_rows':
                blank_mapping = {
                    'involved_disaster_training_type': ['No'],
                    'knowledge_about_ldcrp': ['No'],
                    'monthly_income': ['15000 to 25000'],
                    'milk_and_products': ['2 to 3'],
                    'pulses': ['2 to 4'],
                    'fruits': ['2 to 3'],
                    'meat_and_fish': ['1']
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
                    'prepared_contingency_plan': ['Yes'],
                    'other_insurance': ['Yes']
                }
                calculateCriteriaScore(question, this_house, yes_mapping)
            elif sample_answer.answer_types in ['keywords', 'varying_data']:
                calculateCriteriaScore(question, this_house)
        elif question.scoring_method == 'code_mapping':
            code_mapping = {'What is status of the household head?':
                            {
                                '1': 'Female Leadership',
                                '2': 'Senior Citizen Leadership',
                                '3': 'Children Leadership',
                                '4': 'Single Women Leadership',
                                '5': 'Disabled Member Leadership',
                                '': 'Others',
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
                            },
                            'Damage in House':
                            {
                                'Completely destroyed': 'Completely Destroyed',
                                'House was flooded': 'House was Flooded',
                                'Minor damages in walls': 'Minor damage in walls',
                                'Damage in foundation': 'Damage in Foundation',
                                'Damage in roof': 'Damage in Roof',
                                '': 'No',
                                'nan': 'No',
                                'Death': 'No',
                                'Injured': 'No',
                                'Furniture': 'No',
                                'Land': 'No',
                                'Livestock': 'No',
                                'Crops': 'No',
                                'Food Stock': 'No',
                                'Machineries': 'No',
                            },

                            'Distance from Nearest School':
                            {
                                'Nearby/In a walking distance': 'Nearby/In a walking distance',
                                '15-30 minutes in vehicles': '30 minutes-1hour in vehicles',
                                '30 minutes-1hour in vehicles': '30 minutes-1hour in vehicles',
                                '': 'No',
                                'nan': 'No'
                            },
                            'Building Bye-Laws and Standard Code':
                            {
                                'Yes': 'Comply',
                                '': "Don't Know",
                                'nan': "Don't Know",
                                'No': "Doesn't Comply"
                            },
                            'Distance from Main Road':
                            {
                                'Near to the house': "Near to the house",
                                '15-30 minutes': "30 Minutes - 1hour",
                                '30 minutes-1 hour': '30 Minutes - 1hour',
                                '': "Near to the house",
                                'nan': "Near to the house",
                            },
                            'Time from Nearest Security Forces':
                            {
                                "15-30 minutes": "Less than an hour",
                                "30minutes-1 hour": "Less than an hour",
                                "More than an hour": "More than an hour",
                                '': "Less than an hour",
                                'nan': "Less than an hour",
                            },
                            'What time does it take to reach nearest public tap from house?':
                            {
                                "Near  the house": "Less than 15 mins",
                                "15-30minutes": "15-30mins",
                                "15-30 minutes":"15-30mins",
                                "30minutes-1 hour": "30min-1hr",
                                "More than an hour": "More than an hour",
                                '': "Less than 15 mins",
                                'nan': "Less than 15 mins",
                                'No': "Less than 15 mins",
                            },
                            'Crop Sufficiency':
                            {
                                '': 'less than 3 months',
                                'nan': 'less than 3 months',
                                '3 to 6 months': '3 to 6 months',
                                'More than 3 months': '6 to 9 months',
                                '6 months to 9': '6 to 9 months',
                                '1 year or more': 'more than 1 year',
                            },
                            'Accesss to Market':
                            {
                                '': '30 minutes to 1 hour',
                                'nan': '30 minutes to 1 hour',
                                '5-15 minutes': '5 to 15 minutes',
                                'Near the house': '5 to 15 minutes',
                                '15-30 minutes': '30 minutes to 1 hour',
                                '30 minutes-1 hour': '30 minutes to 1 hour',
                                'more than 1 hour': 'more than 1 hour',
                            },
                            'Land for Agriculture':
                            {
                                '': 'Land Tenants /Mohi / Landless',
                                'nan': 'Land Tenants /Mohi / Landless',
                                'Landless': 'Land Tenants /Mohi / Landless',
                                'less than 1 kattha': 'Less than 1 Kattha',
                                '1-5 kattha': '1 to 5 Kattha',
                                'more than 10 kattha': 'More than 5 Kattha',
                                '1-5 ropani': 'More than 5 Kattha',
                                '5-10 kattha': 'More than 5 Kattha'
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
            else:
                check_phrases = ['Count Given']
            calculateCriteriaScore(question, this_house, check_phrases)


def returnScore(selected_answer, this_question):
    if len(selected_answer) > 1:
        try:
            has_multiple = Answer.objects.get(
                parent_question=this_question, answer_choice__icontains='Multiple')
            this_answer = has_multiple
        except Answer.DoesNotExist:
            this_answer = selected_answer[0]
            for answer in selected_answer:
                if answer.weight > this_answer.weight:
                    this_answer = answer
    elif selected_answer == '':
        this_answer = ''
    else:
        this_answer = selected_answer[0]
    this_score = this_answer.weight * \
        this_question.weight if this_answer != '' else 0
    this_question.calculated_value = this_score
    this_question.save()


def calculateCriteriaScore(*args):
    this_question = args[0]
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
                selected_answer = Answer.objects.filter(
                    parent_question=this_question, answer_choice__icontains=household_answer[0].strip())
                if len(selected_answer) == 0:
                    selected_answer = Answer.objects.annotate(answer_field=Value(household_answer[0].strip(), output_field=CharField(
                    ))).filter(parent_question=this_question, answer_field__icontains=F('answer_choice'))
                selected_answer = '' if len(
                    selected_answer) == 0 else selected_answer
                returnScore(selected_answer, this_question)

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
                    ))).filter(parent_question=this_question, answer_field__icontains=F('answer_choice')).exclude(answer_choice='No')
                    if len(selected_answer) == 0:
                        selected_answer = Answer.objects.filter(
                            parent_question=this_question, answer_choice__icontains=household_answer[0].strip())
                selected_answer = '' if len(
                    selected_answer) == 0 else selected_answer
                returnScore(selected_answer, this_question)
        elif sample_answer[0].answer_types == 'multi_object_row':
            if map_to_model == "HouseHoldData":
                sample_answer = Answer.objects.filter(
                    parent_question=this_question)
                household_answer = args[1].values_list(
                    map_to_field1, flat=True)
                if not '/' in household_answer[0]:
                    selected_answer = Answer.objects.filter(
                        parent_question=this_question, answer_choice__icontains=household_answer[0].strip())
                else:
                    answers_ = [str(ans)
                                for ans in household_answer[0].split('/')]
                    answers = [ans.split(' ') for ans in answers_]
                    answers = list(flatten(answers))
                    answers = list(filter(None, answers))
                    selected_answer_list = []
                    for ans in answers:
                        this_answer = Answer.objects.filter(
                            parent_question=this_question, answer_choice__icontains=ans)
                        selected_answer_list.append(this_answer[0].pk)
                    selected_answer_list = list(set(selected_answer_list))
                    lowest_weight = 0
                    selected_answer = this_answer
                    for item in selected_answer_list:
                        this_item = Answer.objects.filter(id=int(item))
                        if this_item[0].weight < lowest_weight:
                            selected_answer = this_item
                selected_answer = '' if len(
                    selected_answer) == 0 else selected_answer
                returnScore(selected_answer, this_question)

    elif this_question.scoring_method == "multifield_substring":
        map_to_field1 = this_question.map_to_field_1
        map_to_field2 = this_question.map_to_field_2
        map_to_model = this_question.map_to_model
        if map_to_model == "OwnerFamilyData":
            sample_answer = Answer.objects.filter(
                parent_question=this_question)
            if sample_answer[0].answer_types == 'complex_calculation':
                owner_families = OwnerFamilyData.objects.filter(
                    parent_index=args[1][0].index).values_list(map_to_field1, map_to_field2)
                if map_to_field1 == 'status_of_family_member':
                    for member in owner_families:
                        if member[0] == "People with disability":
                            selected_answer = Answer.objects.annotate(disability_type=Value(member[1], output_field=CharField(
                            ))).filter(parent_question=this_question, disability_type__icontains=F('answer_choice'))
                            selected_answer = '' if len(
                                selected_answer) == 0 else selected_answer
                            returnScore(selected_answer, this_question)
                if map_to_field1 == 'parent_index':
                    dependent = 0
                    for member in owner_families:
                        if "student" in member[1].lower() or "other" in member[1].lower():
                            dependent = dependent+1
                    dependency_ratio = dependent / \
                        owner_families.count() if not owner_families.count() == 0 else 0.99
                    possible_answers = Answer.objects.filter(
                        parent_question=this_question)
                    for answer in possible_answers:
                        current_answer = answer.answer_choice
                        if current_answer.startswith('more'):
                            lower_limit_list = [num for num in current_answer.split(
                                'than')]
                            limit = float(lower_limit_list[1])
                            if dependency_ratio > limit:
                                selected_answer = answer
                        elif current_answer.startswith('less'):
                            upper_limit_list = [num for num in current_answer.split(
                                'than')]
                            limit = float(upper_limit_list[1])
                            if dependency_ratio < limit:
                                selected_answer = answer
                        elif 'to' in current_answer:
                            limit_list = [num for num in current_answer.split(
                                'to')]
                            lower_limit = float(limit_list[0])
                            upper_limit = float(limit_list[1])
                            if dependency_ratio >= lower_limit and dependency_ratio <= upper_limit:
                                selected_answer = answer
                    selected_answer_qset = sample_answer.filter(
                        answer_choice=selected_answer.answer_choice)
                    selected_answer = '' if len(
                        selected_answer_qset) == 0 else selected_answer_qset
                    returnScore(selected_answer, this_question)
        if map_to_model == "AnimalDetailData":
            if map_to_field1 == 'animal_number':
                animal_data = AnimalDetailData.objects.filter(
                    parent_index=args[1][0].index).values_list(map_to_field1, map_to_field2)
                for data_ in animal_data:
                    if data_[0] == '' or data_[0] == None or data_[0] == 'nan':
                        selected_answer = Answer.objects.filter(
                            parent_question=this_question, answer_choice='No')
                    elif int(float(data_[0])) == 0:
                        selected_answer = Answer.objects.filter(
                            parent_question=this_question, answer_choice='No')
                    elif int(float(data_[0])) > 0:
                        if data_[1] == 'No' or data_[1] == '' or data_[1] == None or data_[1] == 'nan':
                            selected_answer = Answer.objects.filter(
                                parent_question=this_question, answer_choice='Yes but not significant')
                        else:
                            selected_answer = Answer.objects.filter(
                                parent_question=this_question, answer_choice='	Yes for Commercial Purpose')
                    else:
                        selected_answer = Answer.objects.filter(
                            parent_question=this_question, answer_choice='No')
                    selected_answer = '' if len(
                        selected_answer) == 0 else selected_answer
                    returnScore(selected_answer, this_question)

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
                selected_answer = '' if len(
                    selected_answer) == 0 else selected_answer
                returnScore(selected_answer, this_question)
            elif sample_answer[0].answer_types == 'varying_data':
                owner_families = OwnerFamilyData.objects.filter(
                    parent_index=args[1][0].index).values_list(this_question.map_to_field_1)
                keyword = 'Yes'
                for member in owner_families:
                    if member[0] == '' or member[0] == 'nan' or member[0] == None:
                        keyword = 'No'
                selected_answer = Answer.objects.filter(
                    parent_question=this_question, answer_choice=keyword)
                selected_answer = '' if len(
                    selected_answer) == 0 else selected_answer
                returnScore(selected_answer, this_question)
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
                selected_answer = '' if len(
                    selected_answer) == 0 else selected_answer
                returnScore(selected_answer, this_question)
            elif sample_answer[0].answer_types == 'keywords':
                household_answer = args[1].values_list(
                    map_to_field1, flat=True)
                keyword = 'No'
                if household_answer[0] == 'Yes':
                    keyword = household_answer[0]
                selected_answer = Answer.objects.filter(
                    parent_question=this_question, answer_choice=keyword)
                selected_answer = '' if len(
                    selected_answer) == 0 else selected_answer
                returnScore(selected_answer, this_question)
            elif sample_answer[0].answer_types == 'varying_data':
                household_answer = args[1].values_list(
                    map_to_field1, flat=True)
                if household_answer[0] == '' or household_answer[0] == 'nan' or household_answer[0] == None:
                    keyword = 'No'
                else:
                    keyword = 'Yes'
                selected_answer = Answer.objects.filter(
                    parent_question=this_question, answer_choice=keyword)
                selected_answer = '' if len(
                    selected_answer) == 0 else selected_answer
                returnScore(selected_answer, this_question)
    elif this_question.scoring_method == "code_mapping":
        map_to_field1 = this_question.map_to_field_1
        map_to_model = this_question.map_to_model
        if map_to_model == "HouseHoldData":
            sample_answer = Answer.objects.filter(
                parent_question=this_question)
            if sample_answer[0].answer_types == 'code_mapping':
                household_answer = args[1].values_list(
                    map_to_field1, flat=True)
                selected_answer = Answer.objects.none()
                if household_answer.count() > 1:
                    for element in household_answer:
                        selected_answer |= Answer.objects.filter(
                            parent_question=this_question, answer_choice__icontains=element)
                else:
                    selected_answer = Answer.objects.filter(
                        parent_question=this_question, answer_choice__icontains=household_answer[0].strip())
                selected_answer = '' if len(
                    selected_answer) == 0 else selected_answer
                returnScore(selected_answer, this_question)
            elif sample_answer[0].answer_types == 'substrings':
                this_owner_answer = []
                household_answer = args[1].values_list(
                    map_to_field1, flat=True)
                selected_answer = Answer.objects.none()
                for answer in args[2][this_question.question]:
                    multi_household_answer = [ans for ans in household_answer[0].split(',')]
                    for this_household_answer in multi_household_answer:
                        if this_household_answer.strip() in answer:
                            this_owner_answer.append(
                                args[2][this_question.question][answer])
                if len(this_owner_answer) > 1:
                    selected_answer = Answer.objects.filter(
                        parent_question=this_question, answer_choice__icontains='Multiple')
                else:
                    selected_answer = Answer.objects.filter(
                        parent_question=this_question, answer_choice__icontains=this_owner_answer[0])
                selected_answer = '' if len(
                    selected_answer) == 0 else selected_answer
                returnScore(selected_answer, this_question)

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
                    parent_question=this_question, answer_choice__iexact=household_answer[0].strip())
                selected_answer = '' if len(
                    selected_answer) == 0 else selected_answer
                returnScore(selected_answer, this_question)
        if sample_answer[0].answer_types == 'substrings':
            if map_to_model == "HouseHoldData":
                household_answer = args[1].values_list(
                    map_to_field1, flat=True)
                selected_answer = Answer.objects.filter(
                    parent_question=this_question, answer_choice__iexact=household_answer[0])
                selected_answer = '' if len(
                    selected_answer) == 0 else selected_answer
                returnScore(selected_answer, this_question)

    elif this_question.scoring_method == "range_based":
        map_to_field1 = this_question.map_to_field_1
        map_to_field2 = this_question.map_to_field_2
        map_to_model = this_question.map_to_model
        sample_answer = Answer.objects.filter(
            parent_question=this_question)
        if sample_answer[0].answer_types == 'with_blank_rows':
            if map_to_model == "HouseHoldData":
                household_answer = args[1].values_list(
                    map_to_field1, flat=True)[0]
                splitted_answer = splitIntStr(household_answer)
                this_value = splitted_answer[0]
                data_type = splitted_answer[1]
                if household_answer == '' or household_answer == 'nan' or household_answer == None:
                    selected_answer = Answer.objects.filter(
                        parent_question=this_question, answer_choice__in=args[2][map_to_field1])
                else:
                    possible_answers = Answer.objects.filter(
                        parent_question=this_question)
                    for answer in possible_answers:
                        current_answer = answer.answer_choice
                        if len(current_answer) == 1:
                            if int(current_answer) == this_value:
                                selected_answer = answer
                        elif current_answer.startswith('more'):
                            lower_limit_list = returnNum(
                                current_answer, 'more_than')
                            limit = lower_limit_list[0]
                            if this_value > limit:
                                selected_answer = answer
                        elif current_answer.startswith('less'):
                            upper_limit_list = returnNum(
                                current_answer, 'less_than')
                            limit = upper_limit_list[0]
                            if this_value < limit:
                                selected_answer = answer
                        elif 'to' in current_answer:
                            limit_list = returnNum(current_answer, 'to')
                            lower_limit = limit_list[0]
                            upper_limit = limit_list[1]
                            if this_value >= lower_limit and this_value <= upper_limit:
                                selected_answer = answer
                    selected_answer = sample_answer.filter(
                        answer_choice=selected_answer.answer_choice)
                selected_answer = '' if len(
                    selected_answer) == 0 else selected_answer
                returnScore(selected_answer, this_question)
        elif sample_answer[0].answer_types == 'complex_calculation':
            if map_to_model == "HouseHoldData":
                household_answer = args[1].values_list(
                    map_to_field1, flat=True)[0]
                size_of_household = OwnerFamilyData.objects.filter(
                    parent_index=household_answer).count()
                size_of_household = size_of_household + 1
                if household_answer == '' or household_answer == 'nan' or household_answer == None:
                    selected_answer = Answer.objects.filter(
                        parent_question=this_question, answer_choice__in=args[2][map_to_field1])
                else:
                    possible_answers = Answer.objects.filter(
                        parent_question=this_question)
                    for answer in possible_answers:
                        current_answer = answer.answer_choice
                        if len(current_answer) == 1:
                            if int(current_answer) == size_of_household:
                                selected_answer = answer
                        elif current_answer.startswith('more'):
                            lower_limit_list = [int(num) for num in current_answer.split(
                                'than') if num.strip().isnumeric()]
                            limit = lower_limit_list[0]
                            if size_of_household > limit:
                                selected_answer = answer
                        elif current_answer.startswith('less'):
                            upper_limit_list = [int(num) for num in current_answer.split(
                                'than') if num.strip().isnumeric()]
                            limit = upper_limit_list[0]
                            if size_of_household < limit:
                                selected_answer = answer
                        elif 'to' in current_answer:
                            limit_list = [int(num) for num in current_answer.split(
                                'to') if num.strip().isnumeric()]
                            lower_limit = limit_list[0]
                            upper_limit = limit_list[1]
                            if size_of_household >= lower_limit and size_of_household <= upper_limit:
                                selected_answer = answer
                    selected_answer = sample_answer.filter(
                        answer_choice=selected_answer.answer_choice)
                selected_answer = '' if len(
                    selected_answer) == 0 else selected_answer
                returnScore(selected_answer, this_question)
