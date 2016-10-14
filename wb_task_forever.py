#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Django specific settings
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Weibo.settings")

import django
if django.VERSION >= (1, 7):#自动判断版本
    django.setup()

# Ensure settings are read
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# Your application specific imports
from web import models

# Models you hava
# x = models.UserProfile.objects.get(name='alex')
# print(x)

"""
from core.Backends import db_method
from web import models
print('get id:', models.Weibo.objects.get(user=2).id)
"""

from core.Backends import wb_handle
n = wb_handle.wb_handle()
n.watch_new_wbs()
