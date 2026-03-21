from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import AgentAssetDetail, AssetViewSet, AgentRegisterAsset


router = DefaultRouter()
router.register(r'assets', AssetViewSet, basename='assets')


urlpatterns = [
    path('', include(router.urls)),

    path('assets/agent/<str:serial>/', AgentAssetDetail.as_view(), name='agent-asset-detail'),
    path('assets/agent/register/', AgentRegisterAsset.as_view(), name='agent-register'),  
    path('assets/agent/register/<str:serial>/', AgentRegisterAsset.as_view(), name='agent-update') 
]