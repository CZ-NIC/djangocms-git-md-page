from tempfile import mkdtemp
from unittest.mock import call, patch

from django.test import TestCase
from git import CommandError

from git_md_page.forms.git_plugins import GitRepositoryForm


class GitRepositoryFormTest(TestCase):
    @patch("git_md_page.forms.git_plugins.mkdtemp")
    @patch("git_md_page.forms.git_plugins.Repo")
    def test_clean_success(self, repo_mock, mkdtemp_mock):
        form = GitRepositoryForm(
            data={
                "URL": "https://example.com/",
                "branch": "main",
                "secret": "DoNotTell",
            }
        )

        temp_folder = mkdtemp()
        mkdtemp_mock.return_value = temp_folder
        validity = form.is_valid()

        self.assertTrue(validity)
        self.assertFalse(form.has_error("URL"))
        self.assertEqual(
            repo_mock.mock_calls,
            [call.clone_from("https://example.com/", temp_folder, env={"GIT_TERMINAL_PROMPT": "0"}, depth=1)],
        )

    @patch("git_md_page.forms.git_plugins.mkdtemp")
    @patch("git_md_page.forms.git_plugins.Repo.clone_from", side_effect=CommandError("Error", status=128))
    def test_clean_failure(self, repo_mock, mkdtemp_mock):
        form = GitRepositoryForm(
            data={
                "URL": "https://example.com/",
                "branch": "main",
                "secret": "DoNotTell",
            }
        )

        temp_folder = mkdtemp()
        mkdtemp_mock.return_value = temp_folder
        validity = form.is_valid()

        self.assertFalse(validity)
        self.assertEqual(form.errors, {"URL": ["Cmd('Error') failed due to: exit code(128)\n  cmdline: Error"]})
        self.assertEqual(
            repo_mock.mock_calls,
            [call.clone_from("https://example.com/", temp_folder, env={"GIT_TERMINAL_PROMPT": "0"}, depth=1)],
        )
