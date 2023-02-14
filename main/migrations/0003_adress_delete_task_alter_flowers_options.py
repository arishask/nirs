# Generated by Django 4.1.4 on 2023-01-22 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_flowers_alter_task_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Adress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='адрес')),
                ('task', models.IntegerField(verbose_name='номер телефона')),
            ],
            options={
                'verbose_name': 'Задача',
                'verbose_name_plural': 'Задачи',
            },
        ),
        migrations.DeleteModel(
            name='Task',
        ),
        migrations.AlterModelOptions(
            name='flowers',
            options={'verbose_name': 'Цветы', 'verbose_name_plural': 'Цветы'},
        ),
    ]