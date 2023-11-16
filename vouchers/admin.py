# admin.py

from django.contrib import admin
from .models import Restaurant, Voucher, Customer, Wallet, VoucherInWallet

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('pk','name',)

@admin.register(Voucher)
class VoucherAdmin(admin.ModelAdmin):
    list_display = ('restaurant', 'buy_amount', 'get_amount', 'is_active')
    list_filter = ('restaurant', 'is_active')
    search_fields = ('restaurant__name',)

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('pk','name',)

@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('customer', 'balance')

@admin.register(VoucherInWallet)
class VoucherInWalletAdmin(admin.ModelAdmin):
    list_display = ('voucher', 'wallet')
