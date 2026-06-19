from drf_spectacular.utils import OpenApiResponse, extend_schema

from apps.Chat.api.v1.serializers import (
    DropdownNatureSerializer,
    ListMessageSerializer,
    MessageSerializer,
    ChatSerializer,
    StartChatSerializerInput,
    StartChatSerializerResponseOutput,
    ParticipantSerializer,
)

list_chats_doc = extend_schema(
    tags=["Chat"],
    summary="List Chats",
    description="List all chat chats of a participant base on its user id",
    responses={
        200: OpenApiResponse(
            response=ChatSerializer(many=True),
            description="List all the chats succesfully",
        ),
    },
)

start_chat_doc = extend_schema(
    tags=["Chat"],
    summary="Create Chat with Participants",
    description="Create or retrieve a chat and assign participants whether its agent or user",
    request=StartChatSerializerInput,
    responses={
        200: OpenApiResponse(
            response=StartChatSerializerResponseOutput,
            description="Chat created or retrieve succesfully",
        ),
    },
)

list_messages_from_chat = extend_schema(
    tags=["Chat"],
    summary="List Chat Messages",
    description="List all the messages from a chat",
    responses={
        200: OpenApiResponse(
            response=ListMessageSerializer,
            description="List of messages retrive succesfully",
        ),
    },
)

list_participants_from_chat = extend_schema(
    tags=["Chat"],
    summary="List Chat Participants",
    description="List all the participants from a chat",
    responses={
        200: OpenApiResponse(
            response=ParticipantSerializer,
            description="List of participants retrive succesfully",
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

create_message = extend_schema(
    tags=["Message"],
    summary="Create Message",
    description=("Create a message, create its statuses and send websocket events."),
    responses={
        200: OpenApiResponse(
            response=MessageSerializer,
            description="Message created succesfully",
        )
    },
)

update_message = extend_schema(
    tags=["Message"],
    summary="Update Message",
    description=("Update a message, create its statuses and send websocket events."),
    responses={
        200: OpenApiResponse(
            response=MessageSerializer,
            description="Message updated succesfully",
        )
    },
)


partial_update_message = extend_schema(
    tags=["Message"],
    summary="Partial Update Message",
    description=("Update a message, create its statuses and send websocket events."),
    responses={
        200: OpenApiResponse(
            response=MessageSerializer,
            description="Message updated succesfully",
        )
    },
)
