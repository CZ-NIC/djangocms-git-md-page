"""Urls for git_md_page."""
from django.urls import re_path

from .views import git_update_endpoint

urlpatterns = [
    re_path(
        r"^endpoints/git_update/(?P<pk>[0-9]+)/$",
        git_update_endpoint,
        name="git_update_endpoint",
    ),
]
