from django.urls import path

from .views import (ArticlesListView,
                    ArticleCreateView,
                    ArticleDetailsView,
                    LatestArticleFeed
                    )

app_name = "blogapp"

urlpatterns = [
    path("list/", ArticlesListView.as_view(), name="blog_list"),
    path("create/", ArticleCreateView.as_view(), name="blog_create"),
    path("blogs/<int:pk>/", ArticleDetailsView.as_view(), name="blog_details"),
    path("blogs/latest/feed", LatestArticleFeed(), name="blogs_feed"),

]

