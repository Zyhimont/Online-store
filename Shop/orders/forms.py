from django import forms
from.models import *


class CheckoutContactForm(forms.Form):
    name = forms.CharField(required=True)
    phone = forms.CharField(required=True)
    address = forms.CharField(required=True)
    email = forms.CharField(required=False)
    comments = forms.CharField(required=False)
