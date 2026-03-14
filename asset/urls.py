from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import AssetViewSet, AgentRegisterAsset


router = DefaultRouter()
router.register(r'assets', AssetViewSet, basename='assets')


urlpatterns = [

    path('', include(router.urls)),

    path(
        'assets/agent/register/',
        AgentRegisterAsset.as_view(),
        name='agent-register'
    ),

]