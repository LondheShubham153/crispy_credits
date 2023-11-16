from rest_framework import serializers
from .models import Voucher, Customer, Wallet, VoucherInWallet

class VoucherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voucher
        fields = '__all__'

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = '__all__'

class VoucherInWalletSerializer(serializers.ModelSerializer):
    voucher = VoucherSerializer()

    class Meta:
        model = VoucherInWallet
        fields = '__all__'
