"""Administration for git_md_page."""

from django.contrib import admin

from git_md_page.forms.git_plugins import GitRepositoryForm
from git_md_page.models import GitRepository


@admin.register(GitRepository)
class GitRepositoryAdmin(admin.ModelAdmin):
    """Admin for GitRepository."""

    model = GitRepository
    form = GitRepositoryForm
