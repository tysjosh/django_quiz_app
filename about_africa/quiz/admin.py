from django.contrib import admin
from .models import *

# Register your models here.


@admin.register(UserProfile)
class UserAdmin(admin.ModelAdmin):
    pass
    list_display = ["user", "country"]


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ["title", "category", "region" , "creation_date"]

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ["prompt", "quiz"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]

@admin.register(QuizResult)
class QuizResultAdmin(admin.ModelAdmin):
    list_display = ["user_profile", "quiz", "score", "quiz_date"]


