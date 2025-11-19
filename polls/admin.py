from django.contrib import admin
from .models import Question, Choice

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1

class QuestionAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at")
    list_filter = ["created_at"]
    search_fields = ["title"]
    inlines = [ChoiceInline]

admin.site.register(Question, QuestionAdmin)
