from django.db import models


# Create your models here.
class Lesson(models.Model):
    name = models.CharField(verbose_name='Название пары', max_length=1000)
    require_comp = models.BooleanField(verbose_name='Нужен компьютерный класс?', default=False)
    is_active = models.BooleanField(verbose_name='Используется?', default=True)

    cabinets = models.ManyToManyField(verbose_name='Кабинеты', to='app.Cabinet')
    teacher = models.ForeignKey(verbose_name='Препод', to='app.Teacher', on_delete=models.SET_NULL, null=True, default=None)

    def __str__(self):
        return f'Пара: {self.name}'

    class Meta:
        verbose_name = 'Пара'
        verbose_name_plural = 'Пары'


class Cabinet(models.Model):
    name = models.IntegerField(verbose_name='Кабинет')
    is_comp = models.BooleanField(verbose_name='Компьютерный кабинет?', default=False)
    is_active = models.BooleanField(verbose_name='Используется?', default=True)

    def __str__(self):
        return f'Кабинет {self.name}'

    class Meta:
        verbose_name = 'Кабинет'
        verbose_name_plural = 'Кабинеты'


class Group(models.Model):
    name = models.CharField(verbose_name='Название группы', max_length=1000)
    max_day = models.IntegerField(verbose_name='Максимум пар за день', default=4)
    is_active = models.BooleanField(verbose_name='Используется?', default=True)

    lessons = models.ManyToManyField(verbose_name='Пары', to='app.Lesson', blank=True)

    def __str__(self):
        return f'Группа {self.name}'

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'


class Teacher(models.Model):
    first_name = models.CharField(verbose_name='Имя', max_length=1000)
    last_name = models.CharField(verbose_name='Фамилия', max_length=1000)
    is_active = models.BooleanField(verbose_name='Используется?', default=True)
