import json

from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.decorators import action, api_view
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
import collections
from base.services.permissions import *
from base.services.serializers import *
from .models import *
from rest_framework import filters

from .services.services import get_favorite_PP, get_favorite_SP, update_rating_after_fpp_inc, \
    update_rating_after_fpp_dec, update_rating_after_fsp_inc, update_rating_after_fsp_dec, sendPackPP, sendPackSP


class GenereViewSet(viewsets.ModelViewSet):
    queryset = Genere.objects.all()
    serializer_class = GenereSerializer
    permission_classes = (IsModerOrReadOnly,)


class InstrumentViewSet(viewsets.ModelViewSet):
    queryset = Instrument.objects.all()
    serializer_class = InstrumentSerializer
    permission_classes = (IsModerOrReadOnly,)


class SytheseizerViewSet(viewsets.ModelViewSet):
    queryset = Instrument.objects.all()
    serializer_class = InstrumentSerializer
    permission_classes = (IsModerOrReadOnly,)


class SamplePackViewSet(viewsets.ModelViewSet):
    queryset = SamplePack.objects.all().order_by('-rating')
    serializer_class = SamplePackSerializer
    permission_classes = (IsOwnerOrReadOnly,)
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name']
    filterset_fields = ['genere_id', 'author_id']

    @action(detail=True, methods=['get'])
    def get_file(self, request, pk=None):
        return sendPackSP(request, pk)


class SampleViewSet(viewsets.ModelViewSet):
    queryset = Sample.objects.all()
    serializer_class = SampleSerializer
    permission_classes = (IsOwnerOrReadOnly,)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['sp_id_id', 'instrument_id']



class PresetPackViewSet(viewsets.ModelViewSet):
    queryset = PresetPack.objects.all()
    serializer_class = PresetPackSerializer
    permission_classes = (IsOwnerOrReadOnly,)
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name']
    filterset_fields = ['genere_id', 'author_id', 'sytheseizer_id']
    parser_classes = (FileUploadParser,)
    @action(detail=True, methods=['get'])
    def get_file(self, request, pk=None):
        return sendPackPP(request, pk)

class PresetViewSet(viewsets.ModelViewSet):
    queryset = Preset.objects.all()
    serializer_class = PresetSerializer
    permission_classes = (IsOwnerOrReadOnly,)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['pp_id_id', 'instrument_id']


class CurentUserFavApiView(APIView):
    def post(self, request):
        serializer = CustomUserGetSerializer(data=request.data)
        serializer.is_valid(raise_exception=False)
        pk = CustomUser.objects.filter(username=serializer.data['username']).values('id')
        pk = pk.values_list('id')[0]
        return JsonResponse(PresetPackSerializer(get_favorite_PP(pk), many=True).data,safe=False)

class CurentUserFavSPApiView(APIView):
    def post(self, request):
        serializer = CustomUserGetSerializer(data=request.data)
        serializer.is_valid(raise_exception=False)
        pk = CustomUser.objects.filter(username=serializer.data['username']).values('id')
        pk = pk.values_list('id')[0]
        return JsonResponse(SamplePackSerializer(get_favorite_SP(pk), many=True).data, safe=False)

class FavoritePresetPackAPIVIEW(APIView):
    def get(self, request,pk):
        return Response({'Favorite Preset Packs': PresetPackSerializer(get_favorite_PP(pk), many=True).data})



    def post(self, request):
        return Response({'posts': update_rating_after_fpp_inc(request)})

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({'ERROR: No pk'})
        update_rating_after_fpp_dec(pk)
        fpp = FavoritePresetPacks.objects.get(id=pk)
        fpp.delete()
        return Response('Content deleted')

class FavoriteSamplePackAPIVIEW(APIView):
    def get(self, request, pk=None):
        return Response({'Favorite Sample Packs': SamplePackSerializer(get_favorite_SP(pk), many=True).data})

    def post(self, request):
        return Response({'posts': update_rating_after_fsp_inc(request)})

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({'ERROR: No pk'})
        update_rating_after_fsp_dec(pk)
        fsp = FavoriteSamplePacks.objects.get(id=pk)
        fsp.delete()
        return Response('Content deleted')

class FavoriteSamplePacksViewSet(viewsets.ModelViewSet):
    queryset = FavoriteSamplePacks.objects.all()
    serializer_class = FavoriteSamplePacksSerializer
    permission_classes = (IsOwnerOrReadOnly,)


class FavoritePresetPacksViewSet(viewsets.ModelViewSet):
    queryset = FavoritePresetPacks.objects.filter()
    serializer_class = FavoritePresetPacksSerializer
    permission_classes = (IsOwnerOrReadOnly,)


class FavoritePacksAPIVIEW(APIView):
    def get(self, request, pk=None):
        return Response({'Favorite Preset Packs': PresetPackSerializer(get_favorite_PP(pk), many=True).data,
                         'Favorite Sample Packs': SamplePackSerializer(get_favorite_SP(pk), many=True).data})


class UserAPIVIEW(generics.ListCreateAPIView):
    # queryset = CustomUser.objects.all()
    # serializer_class = CustomUserSerializer
    def post(self, requset):
        serializer = CustomUserSerializer(data=requset.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except:
            return Response(404)
        refresh = RefreshToken.for_user(user=(CustomUser)(CustomUserSerializer))
        dsa =collections.OrderedDict([("refresh",(str)(refresh)),("access",str(refresh.access_token))])
        return Response(dsa)



class PresetPackAPIVIEW(generics.ListCreateAPIView):
    def post(self, request):

        pk = CustomUser.objects.filter(username=request.data['username']).values('id')
        pk = pk.values_list('id')[0]
        return JsonResponse(PresetPackSerializer(PresetPack.objects.filter(author_id=pk), many=True).data, safe=False)

class SamplePackAPIVIEW(generics.ListCreateAPIView):
    def post(self, request):

        pk = CustomUser.objects.filter(username=request.data['username']).values('id')
        pk = pk.values_list('id')[0]
        return JsonResponse(SamplePackSerializer(SamplePack.objects.filter(author_id=pk), many=True).data, safe=False)


class PresetAPIVIEW(generics.ListCreateAPIView):
    queryset = Preset.objects.values('preset_id',  'name', 'instrument_id_id', 'instrument_id__instrument_name')
    serializer_class = CustomPresetSerializer
    def post(self, request):
        pp=request.data['pp_id']
        p = Preset.objects.filter(pp_id_id=pp).values('preset_id', 'name','instrument_id_id', 'instrument_id__instrument_name')
        return JsonResponse(CustomPresetSerializer(p, many=True).data, safe=False)
