"""Unittests for signals."""
import os
from tempfile import mkdtemp
from unittest.mock import call, patch, sentinel

from django.test import TestCase
from git.exc import CommandError

from git_md_page.models import GitRepository, GitTextPluginModel
from git_md_page.signals.git_update import UpdateSignalError, repo_update, repository_update


def setUpModule():
    """Disconnect the signal for repository update on save."""
    repo_update.disconnect(repository_update, sender=GitTextPluginModel)


def tearDownModule():
    """Reconnect the signal for repository update on save."""
    repo_update.connect(repository_update, sender=GitTextPluginModel)


class RepositoryUpdateTest(TestCase):
    """Unittests for repository_update."""

    @classmethod
    def setUpTestData(cls):
        cls.repository = GitRepository.objects.create(URL="https://example.com/test", branch="master")

    def test_no_files(self):
        with self.assertRaisesRegex(UpdateSignalError, "No files to update"):
            repository_update(sentinel.sender, url="https://example.com/test")

    def test_no_repository(self):
        with self.assertRaisesRegex(UpdateSignalError, "No repository found"):
            repository_update(sentinel.sender, url="https://example.com/nonexistent")

    @patch("git_md_page.signals.git_update.mkdtemp")
    @patch("git_md_page.signals.git_update.Repo")
    def test_with_instance(self, repo_mock, mkdtemp_mock):
        instance = GitTextPluginModel.objects.create(file="test.md", repository=self.repository)
        temp_folder = mkdtemp()
        with open(os.path.join(temp_folder, "test.md"), "w") as git_file:
            git_file.write("test")
        mkdtemp_mock.return_value = temp_folder
        repository_update(sentinel.sender, instance=instance)
        self.assertEqual(
            repo_mock.mock_calls,
            [call.clone_from("https://example.com/test", temp_folder, depth=1)],
        )
        self.assertHTMLEqual(GitTextPluginModel.objects.get(file="test.md").content, "<p>test</p>")

    @patch("git_md_page.signals.git_update.mkdtemp")
    @patch("git_md_page.signals.git_update.Repo")
    def test_failed_clone(self, repo_mock, mkdtemp_mock):
        GitTextPluginModel.objects.create(file="test.md", repository=self.repository)
        temp_folder = mkdtemp()
        repo_mock.clone_from.side_effect = CommandError("test")
        mkdtemp_mock.return_value = temp_folder
        with self.assertRaises(UpdateSignalError):
            repository_update(sentinel.sender, url="https://example.com/test")
        self.assertEqual(
            repo_mock.mock_calls,
            [call.clone_from("https://example.com/test", temp_folder, depth=1)],
        )

    @patch("git_md_page.signals.git_update.mkdtemp")
    @patch("git_md_page.signals.git_update.Repo")
    def test_render(self, repo_mock, mkdtemp_mock):
        GitTextPluginModel.objects.create(file="test.md", repository=self.repository)
        temp_folder = mkdtemp()
        with open(os.path.join(temp_folder, "test.md"), "w") as git_file:
            git_file.write("test")
        mkdtemp_mock.return_value = temp_folder
        repository_update(sentinel.sender, url="https://example.com/test")
        self.assertEqual(
            repo_mock.mock_calls,
            [call.clone_from("https://example.com/test", temp_folder, depth=1)],
        )
        self.assertHTMLEqual(GitTextPluginModel.objects.get(file="test.md").content, "<p>test</p>")

    @patch("git_md_page.signals.git_update.mkdtemp")
    @patch("git_md_page.signals.git_update.Repo")
    def test_render_md(self, repo_mock, mkdtemp_mock):
        GitTextPluginModel.objects.create(file="test.md", repository=self.repository)
        temp_folder = mkdtemp()
        with open(os.path.join(temp_folder, "test.md"), "w") as git_file:
            git_file.write("# test #\n\n" "## list ##\n" "- item\n" "- second item")
        mkdtemp_mock.return_value = temp_folder
        repository_update(sentinel.sender, url="https://example.com/test")
        self.assertEqual(
            repo_mock.mock_calls,
            [call.clone_from("https://example.com/test", temp_folder, depth=1)],
        )
        content = "<h1>test</h1>" "<h2>list</h2>" "<ul>" "<li>item</li>" "<li>second item</li>" "</ul>"
        self.assertHTMLEqual(GitTextPluginModel.objects.get(file="test.md").content, content)