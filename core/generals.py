GENDER_CHOICES = (
        (1, 'Male'),
        (2, 'Female')
    )


from django.db.models import Q
from core.models import HouseHoldData
from django.http import HttpResponse
from core.models import  Municipality
import csv



def edu_matching(lists, query):
    q = Q()
    for edu in lists:
        q |= Q(owner_education__icontains=edu)
    return query.filter(q)


def member_edu_matching(list, query):
    q = Q()
    for edu in list:
        q |= Q(education_level__icontains=edu)

    return query.filter(q)

def compare_age(query):
    q = Q()
    age_list = ['60', '61', '62', '63', '64', '65', '66', '67', '68', '69', '70', '71', '72', '73', '74', '75', '76', '77', '78', '79', '80']
    for age in age_list:
        q |= Q(age_group__icontains=age)
    return query.filter(q)


def export_municipality_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="municipality.csv"'

    writer = csv.writer(response)

    writer.writerow(['name', 'hlcit_code', 'district', 'province'])

    municipalities = queryset.values_list('name', 'hlcit_code', 'district__name', 'province')

    for municipality in municipalities:
        writer.writerow(municipality)

    return response


def export_district_csv(modeladmin, request,queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="district.csv"'

    writer = csv.writer(response)

    writer.writerow(['name'])

    districts = queryset.values_list('name')

    for district in districts:
        writer.writerow(district)

    return response


