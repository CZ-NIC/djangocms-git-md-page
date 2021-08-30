# djangocms-git-md-page

DjangoCMS plugin for displaying a page with markdown in git repository.

## Installation

1. Add the `djangocms-git-md-plugin` into requirements and install it into the environment.

```python
# setup.py
setup(
    install_requires=[
        # ...
        'djangocms-git-md-page @ git+https://github.com/CZ-NIC/djangocms-git-md-page.git',
    ]
)
```

2. Add `git_md_page` into the `INSTALLED_APPS`

```python
# settings.py
INSTALLED_APPS = [
    # ...
    'git_md_page',
]
```

3. Create an entry in `urls` for incoming notifications from GitHub.

```python
# urls.py
urlpatterns = [
    # ...
    url(r'^git_md_page/', include('git_md_page.urls')),
]
```

4. Run migrations

```shell
$ python manage.py migrate
```

## Usage

In the CMS administration, click the `+` symbol to add a new plugin. This plugin is named `Git MD page` and is located
in the `Others` section.

First of all, it is required to select the source repository. One can choose from the available choices or create a new
choice (new source repository) by clicking the `+` symbol next to the select box. Every repository is defined by its
address and branch. In the form, there are hints what value should be used. Also, there is another field called
`secret`. Its default value is a random string which can be left for further usage. This `secret` value is then used for
security purposes in the GitHub administration.

When a repository is successfully selected, next fill the path to the desired MD file.

After that, it is required to set up a _webhook_ in the GitHub project administration. It updates the content of
the plugin every time the content of the file in the repository is changed. In your GitHub project administration, click
`Settings` (horizontal navigation on the top of the page), `Webhooks` (left vertical navigation), `Add webhook` (a
button in the right top corner).

Note: If the item `Webhooks` is not in the vertical navigation, you probably do not have permissions to manage webhooks
and you should ask the project owner to do it or for the permissions.

In the form of a new webhook you set the `Payload URL` to
`https://your.domain/git_md_page/endpoints/git_update/<repository-id>/`. The `your-domain` is the domain where the web
page will be served, the `<repository-id>` will be explained later. Set the `ContentType` to `application/json` and
finally set the `Secret` to the very same value as the `Secret` of the repository in your django-cms web application, as
mentioned before (it should be the random string, by default).

Last thing to mention is the `<repository-id>`. Getting this ID is a little confusing. In the django-cms web
administration edit the repository instance and check the URL address. It should look like
`https://your.domain/en/admin/git_md_page/gitrepository/1/change/?_to_field=id&_popup=1`. The part `gitrepository/1/`
(alias `gitrepository/<repository-id>/`) is important, because it carries the repository identifier, `1`. This
identifier is then used in the `Payload URL` when setting up the webhook, as mentioned before.

For more information about the GitHub webhooks, check the
[documentation](https://docs.github.com/en/developers/webhooks-and-events/webhooks).
