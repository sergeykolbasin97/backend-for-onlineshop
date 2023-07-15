from django.urls import path

from .views import (
    trie_story_view,
    GroupListView,
)

app_name = 'myapiapp'

urlpatterns = [
    path("ts/", trie_story_view, name="ts"),
    path("groups/", GroupListView.as_view(), name="groups"),
]
