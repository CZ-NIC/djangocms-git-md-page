"""Models for Git plugin."""

from functools import partial

from cms.models import CMSPlugin
from django.db import models
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _


class GitRepository(models.Model):
    """Represents a Git repository from which we can pull pages."""

    URL = models.URLField(
        verbose_name=_("URL for the repository"),
        help_text=_("https://github.com/owner-name/repository-name.git URL must be unique to this site."),
        unique=True,
    )
    secret = models.CharField(
        verbose_name=_("Secret for webhook"), max_length=255, default=partial(get_random_string, length=12)
    )
    branch = models.CharField(
        verbose_name=_("Source branch"),
        max_length=63,
        help_text=_("Source branch is usually either master or main."),
    )

    class Meta:
        """Meta class."""

        verbose_name_plural = _("Git repositories")

    def __str__(self):
        """Understandable representation."""
        return "Repository at {} [{}]".format(self.URL, self.branch)


class GitTextPluginModel(CMSPlugin):
    """Model for GitTextPlugin."""

    repository = models.ForeignKey(GitRepository, on_delete=models.CASCADE)
    file = models.CharField(verbose_name=_("Full path to the file in the repository."), max_length=255)
    content = models.TextField()

    def __str__(self):
        """Understandable representation."""
        return "{}".format(self.file)

    def save(self, no_signals=False, *args, **kwargs):
        """Send a signal to fetch content."""
        from git_md_page.signals.git_update import repo_update

        signal_sent = kwargs.pop("signal_sent", False)
        super().save(no_signals=no_signals, *args, **kwargs)
        if not signal_sent:
            # We are triggering a save in the signal, so do not fire again
            repo_update.send(sender=self.__class__, instance=self)
