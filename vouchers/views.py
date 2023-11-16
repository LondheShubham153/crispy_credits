from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from .models import Voucher, Customer, Wallet, VoucherInWallet, Restaurant
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

class VoucherListCreateView(APIView):
    def get(self, request):
        vouchers = Voucher.objects.filter(is_active=True)

        vouchers_data = [{
            'id': voucher.id,
            'restaurant_name': voucher.restaurant.name,
            'buy_amount': voucher.buy_amount,
            'get_amount': voucher.get_amount,
        } for voucher in vouchers]

        response_data = {
            'vouchers': vouchers_data,
        }

        return JsonResponse(response_data)

    def post(self, request):
        restaurant_id = request.POST.get('restaurant_id')
        buy_amount = request.POST.get('buy_amount')
        get_amount = request.POST.get('get_amount')

        if not restaurant_id or not buy_amount or not get_amount:
            return JsonResponse({'error': 'Incomplete data provided'}, status=400)

        restaurant = get_object_or_404(Restaurant, pk=restaurant_id)

        try:
            buy_amount = int(buy_amount)
            get_amount = int(get_amount)
        except ValueError:
            return JsonResponse({'error': 'Invalid buy_amount or get_amount format'}, status=400)

        if buy_amount <= 10:
            return JsonResponse({'error': 'The "buy" price must be greater than $10'}, status=400)
        if get_amount > 2 * buy_amount:
            return JsonResponse({'error': 'The "get" amount cannot be greater than double the "buy" price'}, status=400)
        if get_amount > 5000:
            return JsonResponse({'error': 'The "get" amount cannot exceed $5000'}, status=400)

        voucher,created = Voucher.objects.get_or_create(
            restaurant=restaurant,
            buy_amount=buy_amount,
            get_amount=get_amount,
            is_active=True,
        )
        if created:
            return JsonResponse({'message': 'Voucher created successfully'})
        
        return JsonResponse({'message': 'Same Voucher already exist'})


class VoucherPurchaseView(APIView):

    def post(self, request):
        customer_id = request.data.get('customer_id')
        voucher_id = request.data.get('voucher_id')

        if not customer_id or not voucher_id:
            return Response({'error': 'Incomplete data provided'}, status=400)

        customer = get_object_or_404(Customer, id=customer_id)
        voucher = get_object_or_404(Voucher, id=voucher_id, is_active=True)

        wallet, created = Wallet.objects.get_or_create(customer=customer)

        voucher_in_wallet, created = VoucherInWallet.objects.get_or_create(voucher=voucher, wallet=wallet)
        if created:
            wallet.balance += voucher.get_amount
            wallet.save()

            return Response({'message': f'{voucher} purchased successfully'})
        return Response({'message': f'{voucher} already purchased'})

class VoucherRedeemView(APIView):

    def post(self, request):
        customer_id = request.POST.get('customer_id')
        voucher_id = request.POST.get('voucher_id')
        purchase_amount = request.POST.get('purchase_amount')

        if not customer_id or not voucher_id or not purchase_amount:
            return JsonResponse({'error': 'Incomplete data provided'}, status=400)

        customer = get_object_or_404(Customer, pk=customer_id)
        wallet = get_object_or_404(Wallet, customer=customer)
        voucher_in_wallet = get_object_or_404(VoucherInWallet, wallet=wallet, voucher__id=voucher_id)

        if voucher_in_wallet.is_redeemed:
            return JsonResponse({'error': 'Voucher already redeemed'}, status=400)

        voucher = voucher_in_wallet.voucher

        try:
            purchase_amount = int(purchase_amount)
        except ValueError:
            return JsonResponse({'error': 'Invalid purchase_amount format'}, status=400)



        if voucher.get_amount > purchase_amount:
            if wallet.balance >= voucher.get_amount:
                wallet.balance -= voucher.get_amount
                wallet.save()

                voucher_in_wallet.is_redeemed = True
                voucher_in_wallet.save()

                return JsonResponse({'message': 'Voucher fully redeemed'})
            else:
                return JsonResponse({'error': 'Insufficient funds in the wallet'}, status=400)
        else:
            remaining_balance = purchase_amount - voucher.get_amount

            if wallet.balance >= purchase_amount:
                wallet.balance -= purchase_amount
                wallet.save()

                voucher_in_wallet.is_redeemed = True
                voucher_in_wallet.save()

                return JsonResponse({'message': 'Voucher partially redeemed', 'remaining_balance': remaining_balance})
            else:
                return JsonResponse({'error': 'Insufficient funds in the wallet'}, status=400)


class WalletDetailView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):

        wallet = get_object_or_404(Wallet, pk=pk)
        vouchers = VoucherInWallet.objects.filter(wallet=wallet)

        wallet_data = {
            'customer_id': wallet.customer.id,
            'balance': wallet.balance,
        }

        vouchers_data = [{
            'voucher_id': voucher.voucher.id,
            'restaurant_name': voucher.voucher.restaurant.name,
            'buy_amount': voucher.voucher.buy_amount,
            'get_amount': voucher.voucher.get_amount,
            'is_redeemed': voucher.is_redeemed,
        } for voucher in vouchers]

        response_data = {
            'wallet': wallet_data,
            'vouchers': vouchers_data,
        }

        return JsonResponse(response_data)