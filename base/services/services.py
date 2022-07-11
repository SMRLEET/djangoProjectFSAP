from django.http import FileResponse

from base.models import PresetPack, SamplePack, FavoritePresetPacks, FavoriteSamplePacks
from base.services.serializers import FavoritePresetPacksSerializer, FavoriteSamplePacksSerializer


def get_favorite_PP(pk=None):
    return PresetPack.objects.raw(
        "select base_presetpack.pp_id, base_presetpack.name, base_presetpack.description from base_presetpack where pp_id in (select pp_id_id from base_favoritepresetpacks where user_id = %(pk)s)",
        {"pk": pk})


def get_favorite_SP(pk=None):
    return SamplePack.objects.raw(
        "select base_samplepack.sp_id, base_samplepack.name, base_samplepack.description from base_samplepack where sp_id in (select sp_id_id from base_favoritesamplepacks where user_id= %(pk)s)",
        {"pk": pk})


def update_rating_after_fpp_inc(request):
    serializer = FavoritePresetPacksSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    pp = PresetPack.objects.get(pp_id=serializer.data['pp_id'])
    pp.rating += 1
    pp.save(update_fields=['rating'])
    return serializer.data


def update_rating_after_fpp_dec(pk) -> None:
    pp = PresetPack.objects.get(pp_id=FavoritePresetPacks.objects.get(id=pk).pp_id_id)
    pp.rating -= 1
    pp.save(update_fields=['rating'])


def update_rating_after_fsp_inc(request):
    serializer = FavoriteSamplePacksSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    sp = SamplePack.objects.get(sp_id=serializer.data['sp_id'])
    sp.rating += 1
    sp.save(update_fields=['rating'])
    return serializer.data


def update_rating_after_fsp_dec(pk) -> None:
    sp = SamplePack.objects.get(sp_id=FavoriteSamplePacks.objects.get(id=pk).sp_id_id)
    sp.rating -= 1
    sp.save(update_fields=['rating'])

def sendPackPP(request,pk):
    st=(str)(PresetPack.objects.get(pp_id=pk).path)
    zip=open(st,'rb')
    return FileResponse(zip)

def sendPackSP(request,pk):
    st=(str)(SamplePack.objects.get(sp_id=pk).path)
    zip=open(st,'rb')
    return FileResponse(zip)