from django.urls import path

from .views import (
    AISupportChatView,
    AISupportEscalateView,
    AISupportSolvedView
)

urlpatterns = [

    path(
        'support-ai/chat/',
        AISupportChatView.as_view()
    ),

    path(
        'support-ai/<uuid:session_id>/escalate/',
        AISupportEscalateView.as_view()
    ),

    path(
        'support-ai/<uuid:session_id>/solved/',
        AISupportSolvedView.as_view()
    ),

]