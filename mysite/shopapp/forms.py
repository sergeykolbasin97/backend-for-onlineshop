from django import forms
from django.contrib.auth.models import Group
from django.core import validators
from django.db.models import CharField
from django.forms import Textarea

from .models import Product, Order



class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = 'name', 'description', 'price', 'discount', 'created_by'

class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = 'delivery_address', 'promocode', 'products', 'user'
        widgets = {
            'delivery_address': Textarea(attrs={'cols': 50, 'rows': 2}),
        }
class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name']

class CSVImportForm(forms.Form):
    csv_file = forms.FileField()
