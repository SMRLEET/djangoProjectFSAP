from rest_framework import routers
from base.views import *

genereRouter = routers.SimpleRouter()
genereRouter.register(r'Genere', GenereViewSet)

instrumentRouter = routers.SimpleRouter()
instrumentRouter.register(r'Instrument', InstrumentViewSet)

sytheseizerRouter = routers.SimpleRouter()
sytheseizerRouter.register(r'Sytheseizer', SytheseizerViewSet)

samplePackRouter = routers.SimpleRouter()
samplePackRouter.register(r'SamplePack', SamplePackViewSet)

sampleRouter = routers.SimpleRouter()
sampleRouter.register(r'Sample', SampleViewSet)

presetPackRouter = routers.SimpleRouter()
presetPackRouter.register(r'PresetPack', PresetPackViewSet)

presetRouter = routers.SimpleRouter()
presetRouter.register(r'Preset', PresetViewSet)

favoritePresetPacksRouter = routers.SimpleRouter()
favoritePresetPacksRouter.register(r'FavoritePresetPacks', FavoritePresetPacksViewSet)

favoriteSamplePacksRouter = routers.SimpleRouter()
favoriteSamplePacksRouter.register(r'FavoriteSamplePacks', FavoriteSamplePacksViewSet)