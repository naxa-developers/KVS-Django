GENDER_CHOICES = (
        (1, 'Male'),
        (2, 'Female')
    )


from django.db.models import Q
from core.models import HouseHoldData

def edu_matching(lists):
    print('abc')
    q = Q()
    for edu in lists:
        q |= Q(owner_education__icontains=edu)
    return HouseHoldData.objects.filter(q)
