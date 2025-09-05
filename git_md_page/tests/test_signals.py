"""Unittests for signals."""

import os
from tempfile import mkdtemp
from unittest.mock import call, patch, sentinel

from django.test import TestCase
from git.exc import CommandError

from git_md_page.models import GitRepository, GitTextPluginModel
from git_md_page.signals.git_update import repo_update, repository_update


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

    @patch("git_md_page.signals.git_update.mkdtemp")
    def test_no_files(self, mkdtemp_mock):
        repository_update(sentinel.sender, url="https://example.com/test")
        mkdtemp_mock.assert_not_called()

    @patch("git_md_page.signals.git_update.mkdtemp")
    def test_no_repository(self, mkdtemp_mock):
        repository_update(sentinel.sender, url="https://example.com/nonexistent")
        mkdtemp_mock.assert_not_called()

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
            [
                call.clone_from(
                    "https://example.com/test",
                    temp_folder,
                    env={"GIT_TERMINAL_PROMPT": "0"},
                    multi_options=["--single-branch", "--branch master"],
                    depth=1,
                )
            ],
        )
        self.assertHTMLEqual(GitTextPluginModel.objects.get(file="test.md").content, "<p>test</p>")

    @patch("git_md_page.signals.git_update.mkdtemp")
    @patch("git_md_page.signals.git_update.Repo")
    def test_failed_clone(self, repo_mock, mkdtemp_mock):
        instance = GitTextPluginModel.objects.create(file="test.md", repository=self.repository)
        temp_folder = mkdtemp()
        repo_mock.clone_from.side_effect = CommandError("test", status=128)
        mkdtemp_mock.return_value = temp_folder
        repository_update(sentinel.sender, url="https://example.com/test")
        instance.refresh_from_db()

        self.assertEqual(
            repo_mock.mock_calls,
            [
                call.clone_from(
                    "https://example.com/test",
                    temp_folder,
                    env={"GIT_TERMINAL_PROMPT": "0"},
                    multi_options=["--single-branch", "--branch master"],
                    depth=1,
                )
            ],
        )
        self.assertEqual(instance.content, "Repository could not be cloned! (error code: 128)")

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
            [
                call.clone_from(
                    "https://example.com/test",
                    temp_folder,
                    env={"GIT_TERMINAL_PROMPT": "0"},
                    multi_options=["--single-branch", "--branch master"],
                    depth=1,
                )
            ],
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
            [
                call.clone_from(
                    "https://example.com/test",
                    temp_folder,
                    env={"GIT_TERMINAL_PROMPT": "0"},
                    multi_options=["--single-branch", "--branch master"],
                    depth=1,
                )
            ],
        )
        content = "<h1>test</h1>" "<h2>list</h2>" "<ul>" "<li>item</li>" "<li>second item</li>" "</ul>"
        self.assertHTMLEqual(GitTextPluginModel.objects.get(file="test.md").content, content)

    @patch("git_md_page.signals.git_update.open", side_effect=FileNotFoundError("File not found in the repository."))
    @patch("git_md_page.signals.git_update.Repo")
    def test_file_not_found(self, repo_mock, open_mock):
        instance = GitTextPluginModel.objects.create(file="test.md", repository=self.repository)
        repository_update(sentinel.sender, url="https://example.com/test")

        instance.refresh_from_db()
        self.assertEqual(instance.content, "File not found!")

    @patch("git_md_page.signals.git_update.mkdtemp")
    @patch("git_md_page.signals.git_update.Repo")
    def test_fenced_code_extension(self, repo_mock, mkdtemp_mock):
        instance = GitTextPluginModel.objects.create(file="test.md", repository=self.repository)
        temp_folder = mkdtemp()
        with open(os.path.join(temp_folder, "test.md"), "w") as git_file:
            git_file.write("```\n<html>\n</html>\n```")
        mkdtemp_mock.return_value = temp_folder
        repository_update(sentinel.sender, url="https://example.com/test")

        instance.refresh_from_db()
        self.assertEqual(instance.content, "<pre><code>&lt;html&gt;\n&lt;/html&gt;\n</code></pre>")
