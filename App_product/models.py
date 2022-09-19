from django.db import models
from django_mysql.models import ListCharField

# Create your models here.
from App_login.models import User

season_choice = (
    ('Summer', 'Summer'),
    ('Rainy-Season', 'Rainy-Season'),
    ('Autumn', 'Autumn'),
    ('Late-Autumn', 'Late-Autumn'),
    ('Winter', 'Winter'),
    ('Spring', 'Spring'),
)


class FruitModel(models.Model):
    vendor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vendor')
    main_image = models.ImageField(upload_to='Product_image/')
    image1 = models.ImageField(upload_to='Product_image/')
    image2 = models.ImageField(upload_to='Product_image/')
    image3 = models.ImageField(upload_to='Product_image/')
    name = models.CharField(max_length=264)
    seasons = ListCharField(base_field=models.CharField(max_length=20, choices=season_choice), size=20,
                            max_length=(20 * 50))
    preview_text = models.TextField(max_length=200, verbose_name='Preview Text')
    details_text = models.TextField(max_length=10000, verbose_name='Description')
    availability = models.BooleanField(default=False)
    unit = models.CharField(max_length=100)
    price = models.FloatField(verbose_name='Price per unit')
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name', ]
