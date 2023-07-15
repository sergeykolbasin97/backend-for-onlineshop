from django import forms

from blogapp.models import Article

Article


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = 'title', 'content', 'author', 'category', 'tag'

