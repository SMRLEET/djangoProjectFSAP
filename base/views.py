from django.http import JsonResponse, HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics, mixins, status
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
import collections
from base.services.permissions import *
from base.serializers import *
from .models import *
from rest_framework import filters
from .services.services import \
    update_rating_after_fpp_dec, update_rating_after_fsp_dec, \
    get_favorite_PP, get_favorite_SP, sendPack, destroyPacks


class GenereViewSet(viewsets.ModelViewSet):
    queryset = Genere.objects.all()
    serializer_class = GenereSerializer
    permission_classes = (IsModerOrReadOnly,)


class InstrumentViewSet(viewsets.ModelViewSet):
    queryset = Instrument.objects.all()
    serializer_class = InstrumentSerializer
    permission_classes = (IsModerOrReadOnly,)


class SytheseizerViewSet(viewsets.ModelViewSet):
    queryset = Sytheseizer.objects.all()
    serializer_class = SytheseizerSerializer
    permission_classes = (IsModerOrReadOnly,)


class SamplePackViewSet(viewsets.ModelViewSet):
    queryset = SamplePack.objects.all().order_by('-rating')
    serializer_class = SamplePackSerializer
    permission_classes = (IsOwnerOrReadOnly,)
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name']
    filterset_fields = ['genere_id', 'author_id']

    @action(detail=True, methods=['get'])
    def get_file(self, request, pk=None):
        return sendPack(request, SamplePack.objects.get(sp_id=pk).path)

    @action(detail=True, methods=['get'])
    def get_example(self, request, pk=None):
        return sendPack(request, SamplePack.objects.get(sp_id=pk).example)

    def destroy(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return HttpResponse('No pk', status=416)
        return destroyPacks(SamplePack, pk)


class SampleViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Sample.objects.all()
    serializer_class = SampleSerializer
    permission_classes = (IsOwnerOrReadOnly,)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['sp_id_id', 'instrument_id']

    def create(self, request, *args, **kwargs):
        is_many = isinstance(request.data, list)
        if not is_many:
            return super(SampleViewSet, self).create(request, *args, **kwargs)
        else:
            serializer = self.get_serializer(data=request.data, many=True)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class PresetPackViewSet(viewsets.ModelViewSet):
    queryset = PresetPack.objects.all()
    serializer_class = PresetPackSerializer
    permission_classes = (IsOwnerOrReadOnly,)
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name']
    filterset_fields = ['genere_id', 'author_id', 'sytheseizer_id']

    @action(detail=True, methods=['get'])
    def get_file(self, request, pk=None):
        return sendPack(request, PresetPack.objects.get(pp_id=pk).path)

    @action(detail=True, methods=['get'])
    def get_example(self, request, pk=None):
        return sendPack(request, PresetPack.objects.get(pp_id=pk).example)

    def destroy(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return HttpResponse('No pk', status=416)
        return destroyPacks(PresetPack, pk)


class PresetViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Preset.objects.all()
    serializer_class = PresetSerializer
    permission_classes = (IsOwnerOrReadOnly,)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['pp_id_id', 'instrument_id']

    def create(self, request, *args, **kwargs):
        is_many = isinstance(request.data, list)
        if not is_many:
            return super(PresetViewSet, self).create(request, *args, **kwargs)
        else:
            serializer = self.get_serializer(data=request.data, many=True)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CurentUserFavApiView(APIView):

    def get(self, request):
        user = request.user
        queryset = FavoritePresetPacks.objects.filter(user_id=user.id).values('id',
                                                                                                      'user__username',
                                                                                                      'pp_id_id',
                                                                                                      'pp_id__name',
                                                                                                      'pp_id__rating',
                                                                                                      'pp_id__description')
        return JsonResponse(CurentUserFavoritePresetPacksSerializer(queryset, many=True).data, safe=False)


class CurentUserFavSPApiView(APIView):

    def get(self, request):
        user = request.user
        queryset = FavoriteSamplePacks.objects.filter(user_id=user.id).values('id',
                                                                                                      'user__username',
                                                                                                      'sp_id_id',
                                                                                                      'sp_id__name',
                                                                                                      'sp_id__rating',
                                                                                                      'sp_id__description')
        return JsonResponse(CurentUserFavoriteSamplePacksSerializer(queryset, many=True).data, safe=False)


class FavoritePresetPackAPIVIEW(APIView):
    queryset = FavoritePresetPacks.objects.all()
    serializer_class = FavoritePresetPacksSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def check_object_permissions(self, request, obj):
        super().check_object_permissions(request, obj)
        if not IsOwnerOrReadOnly().has_object_permission(request, self, obj):
            raise PermissionError()

    def get_permissions(self):
        if not (self.request.method in permissions.SAFE_METHODS):
            return [permission() for permission in (IsOwnerOrReadOnly,)]
        return super(FavoritePresetPackAPIVIEW, self).get_object_permissions()

    def get(self, request, pk):
        return Response({'Favorite Preset Packs': PresetPackSerializer(get_favorite_PP(pk), many=True).data})

    def post(self, request):

        FavoritePresetPacks.objects.create(pp_id_id=request.data['pp_id'], user_id=request.user.id)

        pp = PresetPack.objects.get(pp_id=request.data['pp_id'])
        pp.rating += 1
        pp.save(update_fields=['rating'])
        return HttpResponse('Created successfully', status=201)

    def delete(self, request, *args, **kwargs):

        pk = kwargs.get("pk", None)
        if not pk:
            return Response({'ERROR: No pk'})
        self.check_object_permissions(request, FavoritePresetPacks.objects.get(pk=pk))
        update_rating_after_fpp_dec(pk)
        fpp = FavoritePresetPacks.objects.get(id=pk)
        fpp.delete()
        return HttpResponse('Deleted successfully', status=204)


class FavoriteSamplePackAPIVIEW(APIView):

    def check_object_permissions(self, request, obj):
        super().check_object_permissions(request, obj)
        if not IsOwnerOrReadOnly().has_object_permission(request, self, obj):
            raise PermissionError()

    def get_permissions(self):
        if not (self.request.method in permissions.SAFE_METHODS):
            return [permission() for permission in (IsOwnerOrReadOnly,)]
        return super(FavoriteSamplePackAPIVIEW, self).get_object_permissions()

    def get(self, request, pk=None):
        return Response({'Favorite Sample Packs': SamplePackSerializer(get_favorite_SP(pk), many=True).data})

    def post(self, request):
        FavoriteSamplePacks.objects.create(sp_id_id=request.data['sp_id'], user_id=request.user.id)
        sp = SamplePack.objects.get(sp_id=request.data['sp_id'])
        sp.rating += 1
        sp.save(update_fields=['rating'])
        return Response({"Added"})

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({'ERROR: No pk'})
        self.check_object_permissions(request, FavoriteSamplePacks.objects.get(pk=pk))
        update_rating_after_fsp_dec(pk)
        fsp = FavoriteSamplePacks.objects.get(id=pk)
        fsp.delete()
        return Response('Content deleted')


class FavoriteSamplePacksViewSet(viewsets.ModelViewSet):
    queryset = FavoriteSamplePacks.objects.all()
    serializer_class = FavoriteSamplePacksSerializer
    permission_classes = (IsOwnerOrReadOnly,)


class FavoritePresetPacksViewSet(viewsets.ModelViewSet):
    queryset = FavoritePresetPacks.objects.all()
    serializer_class = FavoritePresetPacksSerializer
    permission_classes = (IsOwnerOrReadOnly,)


class UserAPIVIEW(generics.ListCreateAPIView):

    def post(self, request):
        CustomUser.objects.create_user(username=request.data['username'], email=request.data['email'],
                                       password=request.data['password'])
        refresh = RefreshToken.for_user(user=(CustomUser)(CustomUserSerializer))
        dsa = collections.OrderedDict([("refresh", (str)(refresh)), ("access", str(refresh.access_token))])
        return Response(dsa)

    def get(self, request):
        if request.GET.get("username", None) is not None:
            username = request.GET.get("username", None)
            return JsonResponse(CustomUserSerializer(CustomUser.objects.filter(username=username), many=True).data,
                                safe=False)
        return HttpResponse('Cannot find user', status=404)


class PresetPackAPIVIEW(generics.ListCreateAPIView):
    def get(self, request):
        user = request.user
        pk = user.id
        return JsonResponse(PresetPackSerializer(PresetPack.objects.filter(author_id=pk), many=True).data, safe=False)


class SamplePackAPIVIEW(generics.ListCreateAPIView):
    def get(self, request):
        user = request.user
        pk = user.id
        return JsonResponse(SamplePackSerializer(SamplePack.objects.filter(author_id=pk), many=True).data, safe=False)


class PresetAPIVIEW(generics.ListCreateAPIView):
    queryset = Preset.objects.values('preset_id', 'name', 'instrument_id_id', 'instrument_id__instrument_name')
    serializer_class = CustomPresetSerializer

    def post(self, request):
        pp = request.data['pp_id']
        p = Preset.objects.filter(pp_id_id=pp).values('preset_id', 'name', 'instrument_id_id',
                                                      'instrument_id__instrument_name')
        return JsonResponse(CustomPresetSerializer(p, many=True).data, safe=False)


class CurrentPresetPackAPIVIEW(generics.ListCreateAPIView):
    queryset = PresetPack.objects.values('pp_id', 'name', 'sytheseizer_id__sytheseizer_name', 'genere_id__genere_name',
                                         'rating', 'description')
    serializer_class = CustomPresetPackSerializer

    def post(self, request):
        pp = request.data['pp_id']
        p = PresetPack.objects.filter(pp_id=pp).values('pp_id', 'name', 'sytheseizer_id__sytheseizer_name',
                                                       'genere_id__genere_name', 'rating', 'description', 'example')
        return JsonResponse(CustomPresetPackSerializer(p, many=True).data, safe=False)


class CurrentSamplePackAPIVIEW(generics.ListCreateAPIView):
    queryset = SamplePack.objects.values('sp_id', 'name', 'genere_id__genere_name',
                                         'rating', 'description')
    serializer_class = CustomSamplePackSerializer

    def post(self, request):
        pp = request.data['sp_id']
        p = SamplePack.objects.filter(sp_id=pp).values('sp_id', 'name',
                                                       'genere_id__genere_name', 'rating', 'description', 'example')
        return JsonResponse(CustomSamplePackSerializer(p, many=True).data, safe=False)


class SampleAPIVIEW(generics.ListCreateAPIView):
    queryset = Sample.objects.values('sample_id', 'name', 'instrument_id_id', 'instrument_id__instrument_name')
    serializer_class = CustomSampleSerializer

    def post(self, request):
        pp = request.data['sp_id']
        p = Sample.objects.filter(sp_id_id=pp).values('sample_id', 'name', 'instrument_id_id',
                                                      'instrument_id__instrument_name')
        return JsonResponse(CustomSampleSerializer(p, many=True).data, safe=False)
