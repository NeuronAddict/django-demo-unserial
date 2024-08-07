from django.contrib import admin

from .models import Comment


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    list_display = ["comment_text", "pub_date", "was_published_recently"]
    search_fields = ["comment_text"]
    list_filter = ["pub_date"]
    fieldsets = [
        (None, {"fields": ["question_text"]}),
        ("Date information", {"fields": ["pub_date"], "classes": ["collapse"]}),
    ]
    inlines = [CommentInline]


admin.site.register(Comment)
