from drf_spectacular.utils import (
    OpenApiResponse,
    extend_schema,
)

from apps.Chat.api.v1.serializers import (
    StartChatSerializerInput,
    StartChatSerializerResponseOutput,
    DropdownNatureSerializer,
)

start_chat_doc = extend_schema(
    tags=["Chat"],
    summary="Create or retrieve a chat and assign particiants",
    description="Create or retrieve a chat and assign participants whether its agent or user",
    request=StartChatSerializerInput,
    responses={
        200: OpenApiResponse(
            response=StartChatSerializerResponseOutput,
            description="Chat created or retrieve succesfully",
        ),
    },
)

list_natures_doc = extend_schema(
    tags=["Nature"],
    summary="List nature options",
    description=(
        "Retrieves a list of all available nature/chat types. "
        "Requires subscription and proper permissions. "
        "No pagination applied."
    ),
    responses={
        200: OpenApiResponse(
            response=DropdownNatureSerializer(many=True),
            description="List of nature options retrieved successfully",
        )
    },
)
