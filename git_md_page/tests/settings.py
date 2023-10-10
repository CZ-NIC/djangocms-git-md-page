import os

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

INSTALLED_APPS = (
    "django.contrib.admin",
    "django.contrib.sites",
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "django.contrib.messages",
    "cms",
    "menus",
    "treebeard",
    "git_md_page",
)

SECRET_KEY = "TOP SECRET"

BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "git_md_page")
TEMPLATES = [
    {
        "APP_DIRS": True,
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    }
]

MIDDLEWARE = [
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
]

ROOT_URLCONF = "git_md_page.urls"

CSRF_FAILURE_VIEW = "django.views.csrf.csrf_failure"

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
        "LOCATION": "/tmp/git_md_page_cache",
    }
}
