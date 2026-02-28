from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Содержание")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_date = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True, verbose_name="Изображение")
    video = models.FileField(upload_to='blog_videos/', blank=True, null=True, verbose_name="Видео")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('post_detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
        ordering = ['-created_date']

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name="Статья")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    text = models.TextField(verbose_name="Комментарий")
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f'Comment by {self.author} on {self.post}'

class UserSurvey(models.Model):
    EXPERIENCE_CHOICES = [
        ('beginner', 'Новичок'),
        ('intermediate', 'Любитель'),
        ('pro', 'Профессионал'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='survey', verbose_name="Пользователь")
    fishing_experience = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES, verbose_name="Опыт в рыбалке")
    favorite_fish = models.CharField(max_length=100, verbose_name="Любимая рыба")
    preferred_gear = models.CharField(max_length=100, verbose_name="Предпочитаемые снасти")
    about_me = models.TextField(blank=True, verbose_name="О себе")

    def __str__(self):
        return f'Survey for {self.user.username}'
