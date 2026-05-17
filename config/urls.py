from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

admin.site.site_header = "Panel de Administración HelpDesk"
admin.site.site_title = "HelpDesk UAS"
admin.site.index_title = "Gestión del Sistema HelpDesk"

urlpatterns = [
    # Django Admin
    path('admin/', admin.site.urls),
    #JWT
    path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # Usuario
    path('', include('user.urls')),
    # Equipo de computo (Inventario)
    path('', include('asset.urls')),
    # Tickets
    path('', include('ticket.urls')),
    # Chat de soporte
    path('', include('ai_support.urls')),
]
