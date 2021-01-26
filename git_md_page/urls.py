"""Urls for git_md_page."""
from django.conf.urls import url

from .views import git_update_endpoint

urlpatterns = [
    url(
        r"^endpoints/git_update/(?P<pk>[0-9]+)/$",
        git_update_endpoint,
        name="git_update_endpoint",
    ),
]
