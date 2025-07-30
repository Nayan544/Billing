import os
import barcode
from barcode.writer import ImageWriter
from django.conf import settings
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    tax_percent = models.FloatField(default=0)
    discount = models.FloatField(default=0)
    stock = models.PositiveIntegerField(default=0)
    barcode_image = models.ImageField(upload_to='barcodes/', blank=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save first to get ID

        # Generate barcode image if not already generated
        if not self.barcode_image:
            EAN = barcode.get_barcode_class('code128')
            code = EAN(f"{self.id:06}", writer=ImageWriter())

            barcode_filename = f"product_{self.id}_barcode.png"
            barcode_path = os.path.join(settings.MEDIA_ROOT, 'barcodes', barcode_filename)
            os.makedirs(os.path.dirname(barcode_path), exist_ok=True)

            code.save(barcode_path[:-4])  # Remove .png added by library

            # Save barcode path to model
            self.barcode_image = f"barcodes/{barcode_filename}"
            super().save(update_fields=['barcode_image'])

    def __str__(self):
        return self.name
