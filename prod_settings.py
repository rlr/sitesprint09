# -*- coding: utf-8 -*-

LOCAL_DEV = False
DEBUG = False
TEMPLATE_DEBUG = DEBUG

#sorl-thumbnail
THUMBNAIL_DEBUG = False

#django-contact-form
DEFAULT_FROM_EMAIL = 'rickyrosario@gmail.com'

MANAGERS = (
    ('Ricky Rosario','rickyrosario@gmail.com'),
)

DATABASE_ENGINE = 'postgresql_psycopg2'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'db_X'             # Or path to database file if using sqlite3.
DATABASE_USER = 'pg_X'             # Not used with sqlite3.
DATABASE_PASSWORD = 'X'         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'ABC'
EMAIL_HOST_PASSWORD = 'ABC'
EMAIL_USE_TLS = True

CACHE_BACKEND = 'memcached://127.0.0.1:11211'
CACHE_MIDDLEWARE_SECONDS = 60*5
CACHE_MIDDLEWARE_KEY_PREFIX = 'rr.'
CACHE_MIDDLEWARE_ANONYMOUS_ONLY = True

### DEBUG-TOOLBAR SETTINGS
DEBUG_TOOLBAR_CONFIG = {
'INTERCEPT_REDIRECTS': False,
}

INTERNAL_IPS = ('127.0.0.1',)

DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.version.VersionDebugPanel',
    'debug_toolbar.panels.timer.TimerDebugPanel',
    'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
    'debug_toolbar.panels.headers.HeaderDebugPanel',
    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
    'debug_toolbar.panels.template.TemplateDebugPanel',
    'debug_toolbar.panels.sql.SQLDebugPanel',
    'debug_toolbar.panels.logger.LoggingPanel',
)

### django-markup
MARKUP_CHOICES = (
    'none',
    'markdown',
  'textile',
)