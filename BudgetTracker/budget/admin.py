from django.contrib import admin
from .models import Category, Transaction, Budget

admin.site.register(Category)
admin.site.register(Transaction)
admin.site.register(Budget)
