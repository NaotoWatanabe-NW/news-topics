from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django_filters.views import FilterView

from .models import Item, Article
from .filters import ItemFilter, ArticleFilter
from .forms import ItemForm, ArticleForm


class ItemFilterView(LoginRequiredMixin, FilterView):
    model = Item
    filterset_class = ItemFilter
    queryset = Item.objects.all().order_by("-created_at")
    strict = False
    paginate_by = 10

    def get(self, request, **kwargs):
        if request.GET:
            request.session["query"] = request.GET
        else:
            request.GET = request.GET.copy()
            if "quety" in request.session.keys():
                for key in request.session["query"].keys():
                    request.GET[key] = request.session["query"][key]
        return super().get(request, **kwargs)


class ItemDetailView(LoginRequiredMixin, DetailView):
    model = Item


class ItemCreateView(LoginRequiredMixin, CreateView):
    model = Item
    form_class = ItemForm
    success_url = reverse_lazy("index")


class ItemUpdateView(LoginRequiredMixin, UpdateView):
    model = Item
    form_class = ItemForm
    success_url = reverse_lazy("index")


class ItemDeleteView(LoginRequiredMixin, DeleteView):
    model = Item
    success_url = reverse_lazy("index")


class ArticleFilterView(LoginRequiredMixin, FilterView):
    model = Article
    filterset_class = ArticleFilter
    queryset = Article.objects.all().order_by("-created_at")
    strict = False
    paginate_by = 10

    def get(self, request, **kwargs):
        if request.GET:
            request.session["query"] = request.GET
        else:
            request.GET = request.GET.copy()
            if "query!" in request.session.keys():
                for key in request.session["query"].keys():
                    request.GET[key] = request.session["query"][key]
        return super().get(request, **kwargs)


class ArticleDetailView(LoginRequiredMixin, DetailView):
    model = Article
