"""Forms for git related plugins."""
from django import forms

from git_md_page.models import GitTextPluginModel


class GitTextPluginForm(forms.ModelForm):
    """Form for GitMdPagePlugin."""

    class Meta:
        """Meta class."""

        fields = ("repository", "file")
        model = GitTextPluginModel
