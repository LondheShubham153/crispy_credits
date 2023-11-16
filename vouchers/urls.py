# your_app/urls.py

from django.urls import path
from .views import VoucherListCreateView, VoucherPurchaseView, VoucherRedeemView, WalletDetailView

app_name = 'vouchers'

urlpatterns = [
    path('vouchers/', VoucherListCreateView.as_view(), name='voucher-list-create'),
    path('purchase/', VoucherPurchaseView.as_view(), name='voucher-purchase'),
    path('redeem/', VoucherRedeemView.as_view(), name='voucher-redeem'),
    path('wallet/<int:pk>/', WalletDetailView.as_view(), name='wallet-detail'),
]
