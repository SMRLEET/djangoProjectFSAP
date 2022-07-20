from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

from base import views

from base.views import *
from base.services import routers, services
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

def home(reauest):
    return HttpResponse('Home page')




urlpatterns = [
    path('admin/',  admin.site.urls),
    path('api/v1/', include(routers.genereRouter.urls)),
    path('api/v1/', include(routers.sytheseizerRouter.urls)),
    path('api/v1/', include(routers.instrumentRouter.urls)),
    path('api/v1/', include(routers.samplePackRouter.urls)),
    path('api/v1/', include(routers.sampleRouter.urls)),
    path('api/v1/', include(routers.presetPackRouter.urls)),
    path('api/v1/', include(routers.presetRouter.urls)),
    path('api/v1/', include(routers.favoritePresetPacksRouter.urls)),
    path('api/v1/', include(routers.favoriteSamplePacksRouter.urls)),

    path('api/v1/FSP/<int:pk>/', FavoriteSamplePackAPIVIEW().as_view()),
    path('api/v1/FSP/', FavoriteSamplePackAPIVIEW().as_view()),
    path('api/v1/FPP/<int:pk>/', FavoritePresetPackAPIVIEW().as_view()),
    path('api/v1/FPP/', FavoritePresetPackAPIVIEW().as_view()),




    path('api/v1/CUPP/', CurentUserFavApiView.as_view()),
    path('api/v1/CUSP/', CurentUserFavSPApiView.as_view()),

    path('api/v1/PresetPackForCurrentUser/', PresetPackAPIVIEW.as_view()),
    path('api/v1/SamplePackForCurrentUser/', SamplePackAPIVIEW.as_view()),

    path('api/v1/CurretPresetPackView/', CurrentPresetPackAPIVIEW.as_view()),
    path('api/v1/CurretSamplePackView/', CurrentSamplePackAPIVIEW.as_view()),

    path('api/v1/getPresets/', PresetAPIVIEW.as_view()),
    path('api/v1/getSamples/', SampleAPIVIEW.as_view()),

    path('api/v1/createuser/', UserAPIVIEW().as_view()),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),


]
