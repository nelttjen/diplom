from django.db import models


# Create your models here.
class Lesson(models.Model):
    name = models.CharField(verbose_name='Название пары', max_length=1000)
    is_active = models.BooleanField(verbose_name='Используется?', default=True)

    cabinet = models.ForeignKey(verbose_name='Кабинеты', to='app.Cabinet', on_delete=models.SET_NULL, null=True, default=None, blank=True)
    teacher = models.ForeignKey(verbose_name='Препод', to='app.Teacher', on_delete=models.SET_NULL, null=True, default=None, blank=True)

    def save(self, *args, **kwargs):
        if not self.cabinet_id or not self.teacher_id:
            self.is_active = False
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Пара: {self.name} - Кабинет {self.cabinet.name}, {self.teacher.__str__()}'

    class Meta:
        db_table = 'lessons'
        verbose_name = 'Пара'
        verbose_name_plural = 'Пары'


class Cabinet(models.Model):
    name = models.CharField(verbose_name='Кабинет', unique=True, max_length=128)

    def __str__(self):
        return f'Кабинет {self.name}'

    class Meta:
        db_table = 'cabinets'
        verbose_name = 'Кабинет'
        verbose_name_plural = 'Кабинеты'
        ordering = ('name', )


class Group(models.Model):
    name = models.CharField(verbose_name='Название группы', max_length=1000)
    max_day = models.IntegerField(verbose_name='Максимум пар за день', default=4)
    is_active = models.BooleanField(verbose_name='Используется?', default=True)

    lessons = models.ManyToManyField(verbose_name='Пары', to='app.Lesson', blank=True)

    def __str__(self):
        return f'Группа {self.name}'

    class Meta:
        db_table = 'groups'
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'


class Teacher(models.Model):
    first_name = models.CharField(verbose_name='Имя', max_length=1000)
    last_name = models.CharField(verbose_name='Фамилия', max_length=1000)
    
    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
    class Meta:
        db_table = 'teachers'
        verbose_name = 'Препод'
        verbose_name_plural = 'Преподы'


class GeneratedLessons(models.Model):
    weekdays = models.JSONField(verbose_name='Рассписание')
    name = models.CharField(verbose_name='Название', max_length=200)

    created_at = models.DateTimeField(verbose_name='Дата создания', editable=False, auto_now_add=True)

    class Meta:
        db_table = 'generated_lessons'

