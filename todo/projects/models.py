from django.db import models

from users.models import User


class Project(models.Model):
    name = models.CharField(max_length=64, verbose_name='Наименование')
    repository_url = models.URLField(verbose_name='Ссылка на репозиторий')
    users = models.ManyToManyField(User, verbose_name='Пользователь')

    def __str__(self):
        return f'{self.name} | {self.repository_url} | {self.users}'


class Todo(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='Проект')
    user = models.ForeignKey(User, on_delete=models.RESTRICT, verbose_name='Пользователь-создатель')
    title = models.CharField(max_length=64, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Заметка')
    is_active = models.BooleanField(verbose_name='активна', default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title} | ({self.project.name}) | {self.user.first_name}'
