from django.db import models
from customers.models import Customer
from products.models import Product
from django.contrib.auth.models import User

class Invoice(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField()

    def total_amount(self):
        return sum(item.total_price() for item in self.items.all())

    def __str__(self):
        return f"Invoice #{self.id} - {self.customer.name}"

class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def unit_price(self):
        return self.product.price 

    def tax_amount(self):
        return (self.unit_price() * self.product.tax_percent / 100) * self.quantity

    def discount_amount(self):
        return (self.unit_price() * self.product.discount / 100) * self.quantity

    def total_price(self):
        return (self.unit_price() * self.quantity) + self.tax_amount() - self.discount_amount()
