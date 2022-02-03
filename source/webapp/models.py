from functools import partial

from django.db import models

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")

    class Meta:
        abstract=True

class Type(models.Model):
    tittle = models.CharField(max_length=100,
                              null=False,
                              blank=False,
                              verbose_name='Тип задачи')

    def __str__(self):
        return f"{self.tittle}"



class Status(models.Model):
    tittle = models.CharField(max_length=100,
                              null=False,
                              blank=False,
                              verbose_name='Статус задачи')

    def __str__(self):
        return f"{self.tittle}"

class Project(models.Model):
    date_start = models.DateField(null=False, blank=False)
    date_end = models.DateField(null=True, blank=True)
    title = models.CharField(max_length=200, null=False, blank=False, verbose_name='Название')
    description = models.TextField(max_length=500, null=False, blank=False, verbose_name='Описание')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        db_table = 'projects'
        verbose_name = 'проект'
        verbose_name_plural = 'проекты'

class Task(BaseModel):
    summary = models.CharField(max_length=200, null=False, blank=False, verbose_name="Заголовок")
    description = models.TextField(max_length=2002, null=True, blank=True, verbose_name="Описание")
    status = models.ForeignKey('webapp.Status', on_delete=models.PROTECT, related_name='status', verbose_name='Статус')
    types = models.ManyToManyField('webapp.Type', related_name='tasks', blank=True)
    project = models.ForeignKey('webapp.Project', on_delete=models.CASCADE, related_name='tasks', verbose_name='Проект')

    def __str__(self):
        return f"{self.pk}. {self.summary}"

    class Meta:
        db_table = 'Tasks'
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

