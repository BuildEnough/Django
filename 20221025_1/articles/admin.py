from django.contrib import admin
from .models import Articles
# asdf
# 1234
# Register your models here.
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')

admin.site.register(Articles, ArticleAdmin)