from django.urls import path, include
from api.viewssets import core_viewsets
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'survey', core_viewsets.SurveyViewSet)
router.register(r'family_members', core_viewsets.FamilyMemberViewSet)
router.register(r'animal_detail', core_viewsets.AnimalViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('province_geo_json', core_viewsets.ProvinceGeojsonViewSet.as_view(), name='province-geojson'),
    path('district_geo_json', core_viewsets.DistrictGeojsonViewSet.as_view(), name='district-geojson'),
    path('municipality_geo_json', core_viewsets.MunicipalityGeojsonViewSet.as_view(), name='municipality-geojson'),
    # path('survey', core_viewsets.SurveyViewSet.as_view(), name='survey'),
    # path('family_members', core_viewsets.F.as_view(), name='survey'),
    # path('survey', core_viewsets.SurveyViewSet.as_view(), name='survey'),
]
