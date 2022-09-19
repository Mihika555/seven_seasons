# Generated by Django 3.2.5 on 2022-03-11 07:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_mysql.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FruitModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('main_image', models.ImageField(upload_to='Product_image/')),
                ('image1', models.ImageField(upload_to='Product_image/')),
                ('image2', models.ImageField(upload_to='Product_image/')),
                ('image3', models.ImageField(upload_to='Product_image/')),
                ('name', models.CharField(max_length=264)),
                ('seasons', django_mysql.models.ListCharField(models.CharField(choices=[('Summer', 'Summer'), ('Rainy-Season', 'Rainy-Season'), ('Autumn', 'Autumn'), ('Late-Autumn', 'Late-Autumn'), ('Winter', 'Winter'), ('Spring', 'Spring')], max_length=20), max_length=1000, size=20)),
                ('preview_text', models.TextField(max_length=200, verbose_name='Preview Text')),
                ('details_text', models.TextField(max_length=10000, verbose_name='Description')),
                ('availability', models.BooleanField(default=False)),
                ('unit', models.CharField(max_length=100)),
                ('price', models.FloatField(verbose_name='Price per unit')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vendor', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
    ]
