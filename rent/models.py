from django.db import models


class RentCategory(models.Model):
    category = models.CharField(max_length=25)
    per = models.DecimalField(decimal_places=2, max_digits=9, null=True)
    amount = models.DecimalField(decimal_places=2, max_digits=9, null=True)
    unit = models.CharField(max_length=25, null=True, blank=True)
    mandetory = models.BooleanField(default=False)


class RentPayment(models.Model):
    month = models.CharField(max_length=50)
    year = models.IntegerField()
    room = models.ForeignKey('tenant.TenantRoom', on_delete=models.CASCADE, related_name='rent')
    total_paid = models.DecimalField(max_digits=9, decimal_places=2, null=True)
    return_amount = models.DecimalField(max_digits=9, decimal_places=2, null=True)
    payment_date = models.DateTimeField(auto_now=False, null=True)
    total_amount = models.DecimalField(max_digits=9, decimal_places=2)
    extra_charge = models.DecimalField(max_digits=9, decimal_places=2, null=True)
    is_paid = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now=False, null=True)


class RentCategoryPayment(models.Model):
    payment = models.ForeignKey(RentPayment, on_delete=models.CASCADE, related_name='rent_category')
    category = models.ForeignKey(RentCategory, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=9, decimal_places=2)
