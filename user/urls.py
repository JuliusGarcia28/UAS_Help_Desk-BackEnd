from django.urls import path
from user.views import Logout

urlpatterns = [
    path('auth/logout/', Logout.as_view(), name='logout'),
]
