from .base import *  # noqa: F403

DEBUG = env_bool("DJANGO_DEBUG", True)  # noqa: F405

# The toolbar is development-only and helps catch query regressions before
# they reach PostgreSQL. API responses remain JSON; inspect requests in its UI.
INSTALLED_APPS += ["debug_toolbar"]  # noqa: F405
MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")  # noqa: F405
INTERNAL_IPS = ["127.0.0.1"]
