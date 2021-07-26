import uuid
from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    category = models.CharField(max_length=50)
    
    def __str__(self):
        return self.category

    class Meta: 
        verbose_name_plural = "Categories"

class Budget(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category)
    allowance = models.FloatField()

    def __str__(self):
        return f'{self.user}, {self.categories.all()}, {self.allowance }'


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, max_length=50, on_delete=models.CASCADE)
    transaction_date = models.DateField()
    amount_spent = models.FloatField()

    def __str__(self):
        return f'{self.user}, {self.category}, {self.transaction_date }, {self.amount_spent}'
