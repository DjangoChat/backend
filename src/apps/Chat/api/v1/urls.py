from django.urls import path

from apps.Chat.api.v1.views import AgentView

urlpatterns = [
    path("agents/", AgentView.as_view(), name="agents-list"),
]
