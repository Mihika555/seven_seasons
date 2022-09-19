from django import forms

from phonenumber_field.widgets import PhoneNumberPrefixWidget
from App_payment.models import BillingAddress
from phonenumber_field.formfields import PhoneNumberField


class BillingForm(forms.ModelForm):
    phone_number = PhoneNumberField(
        widget=PhoneNumberPrefixWidget(initial="BD"),
    )

    class Meta:
        model = BillingAddress
        fields = ['phone_number', 'address', 'zip_code', 'city_zone', 'country']
