from django.db import models
from merchant_api.consts import MAX_DIGITS
from decimal import Decimal
import secrets


class DucatusRootKey(models.Model):
    key_private = models.CharField(max_length=512, unique=True)
    key_public = models.CharField(max_length=512, unique=True)


class MerchantShop(models.Model):
    name = models.CharField(max_length=512, unique=True)
    api_token = models.CharField(max_length=100, default=secrets.token_urlsafe)
    duc_address = models.CharField(max_length=50)
    root_keys = models.ForeignKey(DucatusRootKey, on_delete=models.CASCADE, null=True)


class PaymentRequest(models.Model):
    shop = models.ForeignKey(MerchantShop, on_delete=models.CASCADE, null=True)
    cart_id = models.IntegerField(default=0)
    duc_address = models.CharField(max_length=50, null=True, default=None)
    original_amount = models.DecimalField(max_digits=MAX_DIGITS, decimal_places=0)
    received_amount = models.DecimalField(max_digits=MAX_DIGITS, decimal_places=0, default=Decimal('0'))
    remained_amount = models.DecimalField(max_digits=MAX_DIGITS, decimal_places=0, default=Decimal('0'))
    state = models.CharField(max_length=50, null=True, default='WAITING_FOR_PAYMENT')
    created_at = models.DateTimeField(auto_now_add=True)
    transfer_state = models.CharField(max_length=50, default='NOT_EXECUTED')
    transfer_tx = models.CharField(max_length=100, null=True, default='')

    class Meta:
        unique_together = ('shop', 'cart_id',)
