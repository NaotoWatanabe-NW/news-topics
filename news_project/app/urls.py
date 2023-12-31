from django.urls import path
from .views import ItemFilterView, ItemDetailView, ItemCreateView, ItemUpdateView, ItemDeleteView, ArticleDetailView, ArticleFilterView


urlpatterns = [
    path("", ItemFilterView.as_view(), name="index"),
    path("detail/<int:pk>/", ItemDetailView.as_view(), name="detail"),
    path("create/", ItemCreateView.as_view(), name="create"),
    path("update/<int:pk>/", ItemUpdateView.as_view(), name="update"),
    path("delete/<int:pk>/", ItemDeleteView.as_view(), name="delete"),
    path("filter/<int:pk>/", ItemFilterView.as_view(), name="filter"),
    path("article/<int:pk>/", ArticleDetailView.as_view(), name="article"),
    path("query/<int:pk>/", ArticleFilterView.as_view(), name="query"),
]
