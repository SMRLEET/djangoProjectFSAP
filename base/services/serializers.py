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
    # author = serializers.HiddenField(default=serializers.CurrentUserDefault())
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
    # user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = FavoriteSamplePacks
        fields = "__all__"


class FavoritePresetPacksSerializer(serializers.ModelSerializer):
    # user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = FavoritePresetPacks
        fields = "__all__"


class FavoritePacksModel:
    def __init__(self, id, user_id, pp_id_id, sp_id_id):
        self.id = id
        self.user_id = user_id
        self.pp_id_id = pp_id_id
        self.sp_id_id = sp_id_id


class FavoritePacksSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    user_id = serializers.IntegerField()
    pp_id_id = serializers.IntegerField()
    sp_id_id = serializers.IntegerField()


class CustomUserRegSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('name', 'email', 'password')


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
