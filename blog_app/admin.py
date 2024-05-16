from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from blog_app.models import BlogModel, CommentsModel

# Register your models here.
class SomeModelAdmin(SummernoteModelAdmin):  # instead of ModelAdmin
    summernote_fields = ('text',)

admin.site.register(BlogModel, SomeModelAdmin)
admin.site.register(CommentsModel)