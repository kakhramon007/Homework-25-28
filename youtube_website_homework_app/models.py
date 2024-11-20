from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField


class User_detail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = PhoneNumberField('Phone Number', unique=True)
    email = models.EmailField('Email Address', unique=True)

    def __str__(self):
        return self.user.username


class Video_model(models.Model):
    video_title = models.CharField('Video title', max_length=100)
    video_content = models.FileField(upload_to='video_content/')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='videos')
    like = models.ManyToManyField(User, blank=True, related_name='like_videos')
    dislike = models.ManyToManyField(User, blank=True, related_name='dislike_videos')
    views_count = models.PositiveIntegerField(default=0)
    added_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.video_title


class Comment(models.Model):
    comment = models.TextField('Comment', max_length=2000)
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video_model, on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.comment_user.username} - {self.comment[:50]}'


