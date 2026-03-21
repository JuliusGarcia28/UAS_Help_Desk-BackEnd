from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import AgentAssetDetail, AssetViewSet, AgentRegisterAsset, AgentUpdateAsset

router = DefaultRouter()
router.register(r'inventory', AssetViewSet, basename='assets')

urlpatterns = [

    # Rutas del agente recolector
    path('assets/agent/register/', AgentRegisterAsset.as_view(), name='agent-register'),  
    path('assets/agent/update/<str:serial>/', AgentUpdateAsset.as_view(), name='agent-update'),
    path('assets/agent/<str:serial>/', AgentAssetDetail.as_view(), name='agent-asset-detail'),

    # Router para las operaciones CRUD de Asset
    path('', include(router.urls)),
]