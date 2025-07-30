from django import forms
from .models import Invoice, InvoiceItem
from customers.models import Customer
from products.models import Product
from django.forms.models import inlineformset_factory
from .models import InvoiceItem

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['customer','created_at']
        widgets = {
            'created_at': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }

InvoiceItemFormSet = inlineformset_factory(
    Invoice, InvoiceItem,
    fields=['product', 'quantity'],
    extra=1,
    can_delete=True
)



class InvoiceItemForm(forms.ModelForm):
    class Meta:
        model = InvoiceItem
        fields = ['product', 'quantity']

