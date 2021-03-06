from django.contrib.auth.models import User
from rest_framework import serializers

from base.models import *


class GenereSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genere
        fields = "__all__"


class InstrumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instrument
        fields = "__all__"


class SytheseizerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sytheseizer
        fields = "__all__"


class SamplePackSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = SamplePack
        fields = "__all__"


class SampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sample
        fields = "__all__"


class PresetPackSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = PresetPack
        fields = "__all__"


class PresetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Preset
        fields = "__all__"


class FavoriteSamplePacksSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = FavoriteSamplePacks
        fields = "__all__"


class FavoritePresetPacksSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = FavoritePresetPacks
        fields = "__all__"


class CurentUserFavoritePresetPacksSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    user__username = serializers.CharField()
    pp_id_id = serializers.IntegerField()
    pp_id__name = serializers.CharField()
    pp_id__description = serializers.CharField()
    pp_id__rating = serializers.IntegerField()



class CurentUserFavoriteSamplePacksSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    user__username = serializers.CharField()
    sp_id_id = serializers.IntegerField()
    sp_id__name = serializers.CharField()
    sp_id__description = serializers.CharField()
    sp_id__rating = serializers.IntegerField()



class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'is_superuser')





class CustomPresetSerializer(serializers.Serializer):
    name = serializers.CharField()
    preset_id = serializers.IntegerField()

    instrument_id__instrument_name = serializers.CharField()
    instrument_id_id = serializers.IntegerField()


class CustomPresetPackSerializer(serializers.Serializer):
    pp_id = serializers.IntegerField()
    name = serializers.CharField()
    sytheseizer_id__sytheseizer_name = serializers.CharField()
    genere_id__genere_name = serializers.CharField()
    rating = serializers.IntegerField()
    description = serializers.CharField()
    example = serializers.CharField()

class CustomSamplePackSerializer(serializers.Serializer):
    sp_id = serializers.IntegerField()
    name = serializers.CharField()
    genere_id__genere_name = serializers.CharField()
    rating = serializers.IntegerField()
    description = serializers.CharField()
    example = serializers.CharField()
class CustomSampleSerializer(serializers.Serializer):
    name = serializers.CharField()
    sample_id = serializers.IntegerField()
    instrument_id__instrument_name = serializers.CharField()
    instrument_id_id = serializers.IntegerField()
