from django.test import SimpleTestCase

from git_md_page.models import GitRepository, GitTextPluginModel


class GitRepositoryTest(SimpleTestCase):
    def test_str(self):
        instance = GitRepository(URL="https://example.com/rep.git", secret="secret", branch="master")
        self.assertEqual(str(instance), "Repository at https://example.com/rep.git [master]")


class GitTextPluginModelTest(SimpleTestCase):
    def test_str(self):
        repository = GitRepository(URL="https://example.com/rep.git", secret="secret", branch="master")
        plugin = GitTextPluginModel(repository=repository, file="README.md")
        self.assertEqual(str(plugin), "README.md")
