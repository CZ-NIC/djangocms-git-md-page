"""Forms for git related plugins."""
from shutil import rmtree
from tempfile import mkdtemp

from django import forms
from django.utils.translation import gettext as _
from git import CommandError, Repo

from git_md_page.models import GitRepository, GitTextPluginModel


class GitRepositoryForm(forms.ModelForm):
    """Form for GitRepository model."""

    class Meta:
        """Meta class."""

        fields = "__all__"
        model = GitRepository

    def clean(self):
        """Check repository existence."""
        data = super().clean()

        temp_folder = mkdtemp()
        try:
            Repo.clone_from(data["URL"], temp_folder, env={"GIT_TERMINAL_PROMPT": "0"}, depth=1)
        except CommandError as error:
            self.add_error("URL", str(error))
        finally:
            rmtree(temp_folder)

        return data


class GitTextPluginForm(forms.ModelForm):
    """Form for GitMdPagePlugin."""

    class Meta:
        """Meta class."""

        fields = ("repository", "file")
        model = GitTextPluginModel
