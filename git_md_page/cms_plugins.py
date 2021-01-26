"""Git MD page plugin."""
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext_lazy as _

from git_md_page.forms.git_plugins import GitTextPluginForm
from git_md_page.models import GitTextPluginModel


@plugin_pool.register_plugin
class GitMdPagePlugin(CMSPluginBase):
    """CMS plugin for text from git repository."""

    module = _("Others")
    name = _("Git MD page")
    render_template = "git_md_page/git_text.html"
    model = GitTextPluginModel
    form = GitTextPluginForm
