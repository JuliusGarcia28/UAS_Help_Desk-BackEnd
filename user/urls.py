from django.urls import path
from .views import LoginView, Logout, UserView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [

    path('auth/login/', LoginView.as_view(), name='login'),

    path('auth/logout/', Logout.as_view(), name='logout'),

    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('auth/user/', UserView.as_view(), name='user'),
]