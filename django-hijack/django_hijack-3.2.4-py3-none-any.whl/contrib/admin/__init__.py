import django

if django.VERSION < (3, 2):
    default_app_config = "hijack.contrib.admin.apps.HijackAdminConfig"

from .admin import HijackUserAdminMixin  # noqa
