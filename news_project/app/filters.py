from django_filters import filters
from django_filters import FilterSet
from .models import Item, Article


class MyOrderingFilter(filters.OrderingFilter):
    descending_fmt = "%s"


class ItemFilter(FilterSet):
    name = filters.CharFilter(label="Name", lookup_expr="contains")
    memo = filters.CharFilter(label="Memo", lookup_expr="contains")

    order_by = MyOrderingFilter(
        fields=(("name", "name"), ("age", "age")),
        field_labels={"name": "Name", "age": "Age"},
        label="Order"
    )

    class Meta:
        model = Item
        fields = ("name", "sex", "memo")


class ArticleFilter(FilterSet):
    title = filters.CharFilter(label="Title", lookup_expr="contains")
    article = filters.CharFilter(label="Article", lookup_expr="contains")

    order_by = MyOrderingFilter(
        fields=(("title", "title"), ("article", "article")),
        field_labels={"title": "Title", "article": "Article"},
        label="Order"
    )
    
    class Meta:

        model = Article
        fields = ("title", "article", "url")
