from django.contrib.auth.models import User
from django.db import models
from djmoney.models.fields import MoneyField


class UserProfile(models.Model):
    user: User = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    balance = MoneyField(max_digits=14, decimal_places=2, default_currency='USD', blank=True, null=True)

    def __str__(self):
        return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=30, null=True)
    user: User = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class Transaction(models.Model):
    class TransactionType(models.TextChoices):
        top_up = 'top up', 'top up'
        debit = 'debit', 'debit'

    sum = MoneyField(max_digits=14, decimal_places=2, default_currency='USD', blank=True, null=True)
    time = models.DateTimeField(auto_now_add=True, null=True)
    organization = models.CharField(max_length=30, null=True)
    description = models.CharField(max_length=30, null=True)
    type = models.CharField(max_length=30, choices=TransactionType.choices, null=True)
    category: Category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    user: User = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.organization
