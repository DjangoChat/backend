from rest_framework.pagination import CursorPagination


class ChatPagination(CursorPagination):
    page_size = 50
    page_size_query_param = "page_size"
    ordering = "last_message_at"
