from django.db import models
from django.conf import settings


# Create your models here.
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField


class BillingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='billing_profile')
    phone_number = PhoneNumberField(unique=True, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True)
    zip_code = models.CharField(max_length=20, blank=True)
    city_zone = models.CharField(max_length=50, blank=True)
    country = CountryField(blank_label='(select country)', null=True)

    def __str__(self):
        return f"{self.user.name} billing address"

    def is_full_filled(self):
        fields_name = [f.name for f in self._meta.get_fields()]

        for field in fields_name:
            value = getattr(self, field)
            if value is None or value == "":
                return False
        return True

    class Meta:
        verbose_name_plural = 'BillingAddresses'
