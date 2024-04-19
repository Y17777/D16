from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from ckeditor.fields import RichTextField


class Bullets(models.Model):
    title = models.CharField(max_length=128, verbose_name='Заголовок')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d',
                              verbose_name='Фото', default=None, blank=True, null=True)
    content = RichTextField(blank=True, verbose_name='Контент')
    dateCreation = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Категория')
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL,
                               related_name='posts', null=True, default=None)
    objects = models.Manager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Доска объявлений'
        verbose_name_plural = 'Доска объявлений'
        ordering = ['-dateCreation']
        indexes = [
            models.Index(fields=['-dateCreation'])
        ]

    def get_absolute_url(self):
        return reverse('post', kwargs={'pk': self.pk})


class Category(models.Model):
    name = models.CharField(max_length=128, db_index=True, verbose_name='Категория')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'pk': self.pk})


class UploadFiles(models.Model):
    file = models.FileField(upload_to='uploads')


class Comment(models.Model):
    commentPost = models.ForeignKey(Bullets, on_delete=models.CASCADE, verbose_name='Статья')
    commentAuthor = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор комментария')
    # postAuthor = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, verbose_name='Автор статьи',
    #                                related_name='comments', null=True, default=None)
    text = models.TextField()
    dateCreation = models.DateTimeField(auto_now_add=True)
    accept_status = models.SmallIntegerField(default=0)

    def __str__(self):
        return f'{self.commentAuthor} : {self.text}'

    def get_absolute_url(self):
        return reverse('post', kwargs={'pk': self.commentPost_id})
