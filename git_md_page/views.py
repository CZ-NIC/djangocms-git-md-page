"""Views for git_md_page."""

import hmac
import json

from django.http import HttpResponse, HttpResponseForbidden, HttpResponseNotFound
from django.utils.crypto import constant_time_compare
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from git_md_page.models import GitRepository, GitTextPluginModel
from git_md_page.signals.git_update import repo_update


@csrf_exempt
@require_POST
def git_update_endpoint(request, pk):
    """Validate incoming message and trigger update."""
    # First, get the repository
    try:
        repo = GitRepository.objects.get(pk=pk)
    except GitRepository.DoesNotExist:
        return HttpResponseNotFound("Repository does not exist.")

    # Get the header and verify signature
    sig_header = request.META.get("HTTP_X_HUB_SIGNATURE")
    if sig_header is None:
        return HttpResponseForbidden("No signature")
    signature = "sha1=" + hmac.new(repo.secret.encode(), request.body, digestmod="sha1").hexdigest()
    if not constant_time_compare(signature, sig_header):
        return HttpResponseForbidden("Access denied")

    # Now parse the body for event and check whether or not is the commit on master
    parsed = json.loads(request.body.decode())
    if parsed.get("ref") != "refs/heads/{}".format(repo.branch):
        return HttpResponse("Branch ignored")

    repo_update.send(sender=GitTextPluginModel, url=repo.URL)
    return HttpResponse("Success")
