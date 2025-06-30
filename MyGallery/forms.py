from .models import Product,Comments
from django import forms
 

class ProductForm(forms.ModelForm):
    class Meta:
        model=Product
        fields=['name','description','image']

class commentform(forms.ModelForm):
    class Meta:
        model=Comments
        fields=['name','body']
