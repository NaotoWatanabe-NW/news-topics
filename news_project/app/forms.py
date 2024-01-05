from django import forms
from .models import Item, Article


class ItemForm(forms.ModelForm):

    class Meta:
        model = Item
        fields = {"name", "age", "sex", "memo"}
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "記入例: "}),
            "age": forms.NumberInput(attrs={"min": 1}),
            "sex": forms.RadioSelect(),
            "memo": forms.Textarea(attrs={"rows": 4})
        }


class ArticleForm(forms.ModelForm):

    class Meta:
        model = Article
        fields = {"site", "title", "article", "stored_at", "url"}
        widgets = {
            "site": forms.Textarea(attrs={"cols": 80, "rows": 5}),
            "title": forms.Textarea(attrs={"cols": 80, "rows": 5}),
            "article": forms.Textarea(attrs={"cols": 80, "rows": 20}),
            "stored_at": forms.Textarea(attrs={"cols": 80, "rows": 20}),
            "url": forms.Textarea(attrs={"cols": 80, "rows": 20}),
        }
