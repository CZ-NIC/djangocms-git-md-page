"""Signals for GitRepository update."""
import os
from shutil import rmtree
from tempfile import mkdtemp

from django.dispatch import Signal, receiver
from git import Repo
from git.exc import CommandError
from markdown import markdown

from git_md_page.models import GitRepository, GitTextPluginModel

repo_update = Signal(providing_args=["url", "instance"])


class UpdateSignalError(Exception):
    """Exception from updating of the repositry."""


@receiver(repo_update, sender=GitTextPluginModel)
def repository_update(sender, **kwargs):
    """Perform a repository update and parse all registered files."""
    # Handle the url
    if "instance" in kwargs:
        url = kwargs["instance"].repository.URL
    else:
        url = kwargs["url"]

    # Get the repository
    try:
        repository = GitRepository.objects.get(URL=url)
    except GitRepository.DoesNotExist:
        raise UpdateSignalError("No repository found")

    # Get the files
    files = GitTextPluginModel.objects.filter(repository=repository)
    if not files.exists():
        raise UpdateSignalError("No files to update")

    # Do the update, update content
    temp_folder = mkdtemp()
    try:
        Repo.clone_from(repository.URL, temp_folder, depth=1)
    except CommandError as error:
        raise UpdateSignalError(error)
    else:
        for file in files:
            with open(os.path.join(temp_folder, file.file)) as repo_file:
                file.content = markdown(repo_file.read())
            file.save(signal_sent=True)
    finally:
        rmtree(temp_folder)
