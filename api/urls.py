from django.urls import path, include
from api.viewssets import core_viewsets, user_viewsets
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'house_hold', core_viewsets.HouseHoldViewSet)
router.register(r'family_members', core_viewsets.FamilyDetailViewSet)
router.register(r'animal_detail', core_viewsets.AnimalDetailViewSet)
router.register(r'users', user_viewsets.UserViewSet)
# router.register(r'house_hold', core_viewsets.HouseHoldViewSet)
# router.register(r'animal_detail', core_viewsets.AnimalDetailViewSet)
# router.register(r'owner_family', core_viewsets.FamilyDetailViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('province_geo_json', core_viewsets.ProvinceGeojsonViewSet.as_view(), name='province-geojson'),
    path('district_geo_json', core_viewsets.DistrictGeojsonViewSet.as_view(), name='district-geojson'),
    path('municipality_geo_json', core_viewsets.MunicipalityGeojsonViewSet.as_view(), name='municipality-geojson'),

    # user related urls
    path('auth-token', user_viewsets.CustomAuthToken.as_view(), name='custom_token'),
    path('register', user_viewsets.Register.as_view(), name='register'),
    path('login', user_viewsets.UserLogIn.as_view(), name='login'),
    path('logout', user_viewsets.UserLogOut.as_view(), name='logout'),

    # core_urls
    path('overview', core_viewsets.OverviewViewSet.as_view(), name='overview'),

]
