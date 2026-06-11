from rest_framework.pagination import CursorPagination


class MessagePaination(CursorPagination):
    page_size = 50
    page_size_query_param = "page_size"
    ordering = "sent_at"
