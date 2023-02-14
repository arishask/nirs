from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Flows(models.Model):
    name = models.CharField(max_length=100, verbose_name="Заголовок")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    color = models.CharField(max_length=30, verbose_name="Цвет")
    price = models.PositiveIntegerField(verbose_name="Цена")
    photo = models.ImageField(upload_to="article/", verbose_name="Фото")
    content = models.TextField(default="", blank=True, verbose_name="Описание")
    is_published = models.BooleanField(default=True, verbose_name="Выставить")
    quantity = models.PositiveIntegerField(default=0, blank=True, verbose_name="Остаток на складе")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")

    def __str__(self):
        return self.name + ' ' + self.color

    def get_absolute_url(self):
        return reverse('detail', kwargs={'item_slug': self.slug})

    class Meta:
        verbose_name = 'Цветы'
        verbose_name_plural = 'Цветы'
        ordering = ['time_create']


class ArticleForOrd(models.Model):
    flows = models.ForeignKey('Flows', on_delete=models.PROTECT, verbose_name="Цветы")
    quantity = models.PositiveIntegerField(default=0, blank=True, verbose_name="Количество")
    order = models.ForeignKey('Orders', null=True, on_delete=models.PROTECT)

    def __str__(self):
        return self.flows.name + str(self.quantity)

    class Meta:
        verbose_name = 'Артикул покупки'
        verbose_name_plural = 'Артикулы покупок'
        ordering = ['-id']


class Orders(models.Model):
    date = models.DateTimeField(auto_now_add=True, verbose_name="Дата покупки")
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Заказчик")
    is_paid = models.BooleanField(default=False, verbose_name="Оплата")
    is_took = models.BooleanField(default=False, verbose_name="Получен")

    def __str__(self):
        return self.user.username + str(self.date)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['is_took', 'id']


class Addresses (models.Model):
    address=models.TextField('адрес')
    number=models.CharField('номер', max_length=11)

    def __str__(self):
        return self.address

    class Meta:
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреса'




