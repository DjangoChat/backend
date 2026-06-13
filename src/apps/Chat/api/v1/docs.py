from drf_spectacular.utils import (
    OpenApiResponse,
    extend_schema,
)

from apps.Chat.api.v1.serializers import (
    StartChatSerializerInput,
    StartChatSerializerResponseOutput,
    DropdownNatureSerializer,
    MessageSerializer,
    SimpleChatSerializer,
)

list_chats_doc = extend_schema(
    tags=["Chat"],
    summary="List all the chats of the participant",
    description="List all chat chats of a participant base on its user id",
    responses={
        200: OpenApiResponse(
            response=SimpleChatSerializer(many=True),
            description="List all the chats succesfully",
        ),
    },
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

list_messages_doc = extend_schema(
    tags=["Message"],
    summary="List messages",
    description=(
        "Retrieves a list of 50 messages"
        "Requires chat id and cursor as parameter"
        "Cursos pagination"
    ),
    responses={
        200: OpenApiResponse(
            response=MessageSerializer(many=True),
            description="List of messages retrieved successfully",
        )
    },
)
