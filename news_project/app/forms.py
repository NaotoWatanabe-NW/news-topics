from django import forms
from .models import Item, Article


class ItemForm(forms.ModelForm):

    class Meta:
        model = Item
        field = {"name", "age", "sex", "memo"}
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "記入例: 山田太郎"}),
            "age": forms.NumberInput(attrs={"min": 1}),
            "sex": forms.RadioSelect(),
            "memo": forms.Textarea(attrs={"rows": 4})
        }


class ArticleForm(forms.ModelForm):

    class Meta:
        model = Article
        field = {"site", "title", "article", "stored_at", "url"}
        widgets = {
            "site": forms.Textarea,
            "title": forms.Textarea(),
            "article": forms.Textarea(),
            "stored_at": forms.DateTimeField(),
            "url": forms.CharField(),
        }
