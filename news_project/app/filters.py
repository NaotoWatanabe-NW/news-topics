from django_filters import filters
from django_filters import FilterSet
from .models import Item


class MyOrderingFilter(filters.OrderingFilter):
    descending_fmt = "%s"


class ItemFilter(FilterSet):
    name = filters.CharFilter(label="Name", lookup_expr="contains")
    memo = filters.CharFilter(label="Memo", lookup_expr="contains")
