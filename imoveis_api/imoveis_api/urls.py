from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from imoveis import views


router = routers.DefaultRouter()
router.register('estados', views.EstadoViewSet)
router.register('cidades', views.CidadeViewSet)
router.register('imoveis', views.ImovelViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        'api-auth/',
        include('rest_framework.urls', namespace='rest_framework')
    ),
    path('imoveis_api/', include(router.urls)),
]
