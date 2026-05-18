from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

admin.site.site_header = "Panel de Administracion HelpDesk"
admin.site.site_title = "HelpDesk UAS"
admin.site.index_title = "Gestion del Sistema HelpDesk"

urlpatterns = [
    # Django Admin
    path("admin/", admin.site.urls),
    #JWT
    path("api/token", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # API routes - all prefixed with /api/
    path("api/", include("user.urls")),
    path("api/", include("asset.urls")),
    path("api/", include("ticket.urls")),
    path("api/", include("ai_support.urls")),
]
