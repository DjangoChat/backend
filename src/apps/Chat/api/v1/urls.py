from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.Chat.api.v1.views import ChatView, MessageView, NatureView

router = DefaultRouter()
router.register(r"chats", ChatView, basename="chat")
router.register(r"messages", MessageView, basename="message")
router.register(r"natures", NatureView, basename="nature")


urlpatterns = [
    path("", include(router.urls)),
]
