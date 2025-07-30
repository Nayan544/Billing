from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=100)
    gstin = models.CharField(max_length=15, blank=True)
    contact = models.CharField(max_length=20)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.name
