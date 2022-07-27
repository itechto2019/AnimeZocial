from django.contrib import admin
from . models import Feed, Topic, Like,Comment
# Register your models here.

admin.site.register(Feed)
admin.site.register(Topic)
admin.site.register(Like)
admin.site.register(Comment)
