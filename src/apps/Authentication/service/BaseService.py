from django.db import transaction


class BaseService:

    def transaction(self):
        return transaction.atomic()
