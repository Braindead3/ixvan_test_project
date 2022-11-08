from django_filters import rest_framework as filter

from .models import Transaction


class TransactionsViewSetFilter(filter.FilterSet):
    class Meta:
        model = Transaction
        fields = {
            'time': ['lte', 'gte'],
            'sum': ['lte', 'gte'],
        }
