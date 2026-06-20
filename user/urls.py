from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    LoginView,
    Logout,
    UserView,
    UserViewSet,
    DepartmentViewSet,
    RequestPasswordReset,
    ResetPassword,
    ChangePassword,
    ActivateAccount
)

from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [

    path(
        'auth/login/',
        LoginView.as_view(),
        name='login'
    ),

    path(
        'auth/logout/',
        Logout.as_view(),
        name='logout'
    ),

    path(
        'auth/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),

    path(
        'auth/user/',
        UserView.as_view(),
        name='user'
    ),

    path(
        'auth/request-password-reset/',
        RequestPasswordReset.as_view(),
        name='request_password_reset'
    ),

    path(
        'auth/reset-password/',
        ResetPassword.as_view(),
        name='reset_password'
    ),
    
    
    path(
        'auth/change-password/',
        ChangePassword.as_view(),
        name='change_password'
    ),

    path(
        'auth/activate-account/',
        ActivateAccount.as_view(),
        name='activate_account'
    ),
]

router = DefaultRouter()

router.register(r'users', UserViewSet)
router.register(r'departments', DepartmentViewSet)

urlpatterns += router.urls