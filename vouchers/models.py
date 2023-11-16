from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Voucher(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    buy_amount = models.PositiveIntegerField(validators=[MinValueValidator(11)])
    get_amount = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5000)])
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.restaurant.name} - ${self.buy_amount} Voucher"

class Customer(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.name

class Wallet(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
    balance = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.customer.name}'s Wallet"

class VoucherInWallet(models.Model):
    voucher = models.ForeignKey(Voucher, on_delete=models.CASCADE)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    is_redeemed = models.BooleanField(default=False)  # New field to track redemption status

    def __str__(self):
        return f"{self.wallet.customer.name}'s {self.voucher.restaurant.name} Voucher"
