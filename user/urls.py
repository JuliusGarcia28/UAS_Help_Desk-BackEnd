from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import LoginView, Logout, UserView, UserViewSet, DepartmentViewSet
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [

    path('auth/login/', LoginView.as_view(), name='login'),

    path('auth/logout/', Logout.as_view(), name='logout'),

    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('auth/user/', UserView.as_view(), name='user'),
]

# Admin
router = DefaultRouter()
# Usuarios CRUD
router.register(r'users', UserViewSet)
# Departamentos CRUD
router.register(r'departments', DepartmentViewSet)

urlpatterns += router.urls