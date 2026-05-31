from django.contrib import admin
from pages.models import Subject, Teacher, Article, Comment

# Register your models here.

class TeacherAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "specialty", "is_active")
    list_display_links = ("name",)

class SubjectAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_display_links = ("name", )

class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "approved", "article")
    list_display_links = ("name",)

class ArticleAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "teacher", "subject", "views", "published")
    list_display_links = ("title",)

admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment, CommentAdmin)