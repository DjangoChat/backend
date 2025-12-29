from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from apps.Authentication.api.v1.serializers import LoginSerializer


@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid()
