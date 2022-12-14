# Generated by Django 3.2.5 on 2022-03-11 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NutritionBlogModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blog_title', models.CharField(max_length=100)),
                ('main_image', models.ImageField(upload_to='blog_images/')),
                ('image1', models.ImageField(upload_to='blog_images/')),
                ('image2', models.ImageField(upload_to='blog_images/')),
                ('image3', models.ImageField(upload_to='blog_images/')),
                ('blog', models.TextField()),
                ('created_date', models.DateTimeField(auto_now=True)),
                ('update_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
