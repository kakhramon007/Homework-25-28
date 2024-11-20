from django.contrib import admin
from .models import User_detail, Video_model, Comment


@admin.register(User_detail)
class UserDetailsAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'email')
    search_fields = ('user__username', 'phone_number', 'email')


@admin.register(Video_model)
class VideoModelAdmin(admin.ModelAdmin):
    list_display = ('video_title', 'user', 'views_count', 'added_date')
    search_fields = ('video_title', 'user__username')


@admin.register(Comment)
class CommentModelAdmin(admin.ModelAdmin):
    list_display = ('comment_user', 'video', 'created_at')
    search_fields = ('comment_user__username', 'video__video_title')


# Register your models here.
