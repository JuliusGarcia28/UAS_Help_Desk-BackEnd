from django.urls import path

from .views import (
    AISupportChatView,
    AISupportEscalateView,
    AISupportSolvedView,
    AISupportSessionListView,
    AISupportSessionDetailView
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
    
    path(
        'support-ai/sessions/',
        AISupportSessionListView.as_view()
    ),

    path(
        'support-ai/sessions/<uuid:id>/',
        AISupportSessionDetailView.as_view()
    ),

]