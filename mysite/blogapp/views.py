from django.contrib.syndication.views import Feed
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView

from .models import Article

from .templates.blogapp.forms import ArticleForm


class ArticlesListView(ListView):
    template_name = 'blogapp/article_list.html'
    context_object_name = 'articles'
    queryset = (
        Article.objects
        .filter(pub_date__isnull=False)  # чтобы выдавала только опубликованные статьи
        .order_by('-pub_date')  # чтобы сортировала по свежести статьи
        .select_related("author", "category")
        .prefetch_related("tag")
    )


class ArticleCreateView(CreateView):
    model = Article
    form_class = ArticleForm
    success_url = reverse_lazy('blogapp:blog_list')


class ArticleDetailsView(DetailView):
    template_name = 'blogapp/blog_details.html'
    queryset = Article.objects.defer('title', 'tag').all()
    context_object_name = 'article'

class LatestArticleFeed(Feed):
    title = 'Последние статьи'
    description = 'Последние 5 статей из ленты'
    link = reverse_lazy('blogapp:blog_list')

    def items(self):
        return (
            Article.objects
            .filter(pub_date__isnull=False)
            .order_by('-pub_date')
            .select_related("author", "category")
            .prefetch_related("tag")
        )

    def item_title(self, item: Article):
        return item.title

    def item_description(self, item: Article):
        return item.content[:200]
