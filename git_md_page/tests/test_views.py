"""Unittests for views."""
import hmac
import json
from unittest.mock import Mock, call, patch

from django.test import RequestFactory, TestCase

from git_md_page.models import GitRepository, GitTextPluginModel
from git_md_page.views import git_update_endpoint

MOCK = Mock()


class GitUpdateEndpointTest(TestCase):
    """Unittests for git_update_endpoint."""

    @classmethod
    def setUpTestData(cls):
        cls.repository = GitRepository.objects.create(URL="https://example.com/test", secret="secret", branch="master")

    def test_no_get(self):
        request = RequestFactory().get("/")
        response = git_update_endpoint(request, self.repository.pk)
        self.assertEqual(response.status_code, 405)

    def test_no_repo(self):
        request = RequestFactory().post("/")
        response = git_update_endpoint(request, self.repository.pk + 1)
        self.assertContains(response, "Repository does not exist.", status_code=404)

    def test_no_header(self):
        request = RequestFactory().post("/")
        response = git_update_endpoint(request, self.repository.pk)
        self.assertContains(response, "No signature", status_code=403)

    def test_bad_signature(self):
        request = RequestFactory().post("/")
        request.META["HTTP_X_HUB_SIGNATURE"] = "nonsense"
        response = git_update_endpoint(request, self.repository.pk)
        self.assertContains(response, "Access denied", status_code=403)

    @patch("git_md_page.views.repo_update")
    def test_branch(self, repo_update_mock):
        body = {"ref": "refs/heads/feature"}
        sig = "sha1=" + hmac.new(b"secret", json.dumps(body).encode(), digestmod="sha1").hexdigest()
        request = RequestFactory().post("/", data=body, content_type="application/json")
        request.META["HTTP_X_HUB_SIGNATURE"] = sig
        response = git_update_endpoint(request, self.repository.pk)
        self.assertContains(response, "Branch ignored", status_code=200)
        self.assertEqual(repo_update_mock.mock_calls, [])

    @patch("git_md_page.views.repo_update")
    def test_triggered(self, repo_update_mock):
        body = {"ref": "refs/heads/master"}
        sig = "sha1=" + hmac.new(b"secret", json.dumps(body).encode(), digestmod="sha1").hexdigest()
        request = RequestFactory().post("/", data=body, content_type="application/json")
        request.META["HTTP_X_HUB_SIGNATURE"] = sig
        response = git_update_endpoint(request, self.repository.pk)
        self.assertContains(response, "Success")
        self.assertTrue(
            repo_update_mock.mock_calls,
            [call(sender=GitTextPluginModel, url=self.repository.URL)],
        )
