from django.contrib.auth.models import User
from django.db import models


class Author(models.Model):
    fullname = models.CharField(max_length=150,  verbose_name="Full Name")
    born_date = models.CharField(max_length=150, verbose_name="Born Date")
    born_location = models.CharField(max_length=150, verbose_name="Born Location")
    description = models.TextField(verbose_name="Description")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, default=1, verbose_name="Created By")


    class Meta:
        verbose_name = "Author"
        verbose_name_plural = "Authors"

    def __str__(self):
        return f"{self.fullname}"


class Tag(models.Model):
    name = models.CharField(max_length=300, unique=True, verbose_name="Name")
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)


    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"
        constraints = [
            models.UniqueConstraint(fields=["user", "name"], name="tag of username")
        ]

    def __str__(self):
        return f"{self.name}"


class Quote(models.Model):
    name = models.TextField(verbose_name="Quote")
    tags = models.ManyToManyField(Tag, related_name="quotes", verbose_name="Tags")
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, related_name="author_quotes", verbose_name="Author")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, default=1, verbose_name="Created By")


    class Meta:
        verbose_name = "Quote"
        verbose_name_plural = "Quotes"

    def __str__(self):
        return f"{self.name}"




