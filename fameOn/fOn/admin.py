# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from fOn.models import UserDetail, Post, Comment, Like, Unlike, ProfilePicture
# Register your models here.

admin.site.register(UserDetail)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Unlike)
admin.site.register(ProfilePicture)

