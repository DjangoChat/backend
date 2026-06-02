from django.urls import path

from apps.Chat.api.v1.views import AgentView, NatureDropDownView

urlpatterns = [
    path("agents/", AgentView.as_view(), name="agents-list"),
    path("natures/", NatureDropDownView.as_view(), name="nature-list"),
]
