from django.db import models
from django.core import validators


class Item(models.Model):
    SEX_CHOISE = ((1, "Male"), (2, "Female"))
    name = models.CharField(
        verbose_name="Name",
        max_length=200,
    )
    age = models.IntegerField(
        verbose_name="Age",
        validators=[validators.MinValueValidator(1)],
        blank=True,
        null=True
    )
    sex = models.IntegerField(
        verbose_name="Sex",
        choices=SEX_CHOISE,
        default=1
    )
    memo = models.TextField(
        verbose_name="Memo",
        max_length=300,
    )
    created_at = models.DateTimeField(
        verbose_name="register date",
        auto_now_add=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Item"
        verbose_name_plural = "Item"


class Article(models.Model):
    _id = models.TextField()
    site = models.CharField(
        verbose_name="NewsSite",
        max_length=300,
    )
    title = models.CharField(
        verbose_name="News Title",
        max_length=300,
    )
    article = models.TextField(
        verbose_name="News Article",
    )
    stored_at = models.DateTimeField(
        verbose_name="Stored date"
    )
    url = models.CharField(
        verbose_name="News URL",
        max_length=300,
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Article"
