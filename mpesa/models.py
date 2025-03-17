from django.db import models

# Create your models here.
from django.db import models

class MpesaSTK(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='mpesa_stks', null=True)
    page = models.ForeignKey('mchango.ContributionPage', on_delete=models.CASCADE, related_name='mpesa_stkss', null=True)
    result_desc = models.CharField(max_length=255, null=True, blank=True)
    result_code = models.CharField(max_length=50, null=True, blank=True)
    merchant_request_id = models.CharField(max_length=100, null=True, blank=True)
    checkout_request_id = models.CharField(max_length=100, null=True, blank=True)
    amount = models.CharField(max_length=50, null=True, blank=True)
    trans_id = models.CharField(max_length=100, null=True, blank=True)
    trans_date = models.CharField(max_length=100, null=True, blank=True)
    phonenumber = models.CharField(max_length=15, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"STK Transaction {self.merchant_request_id}"


class MpesaC2B(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='mpesa_c2bs', null=True)
    page = models.ForeignKey('mchango.ContributionPage', on_delete=models.CASCADE, related_name='mpesa_c2bs', null=True)
    trans_type = models.CharField(max_length=100, null=True, blank=True)
    trans_id = models.CharField(max_length=100, null=True, blank=True)
    trans_date = models.CharField(max_length=100, null=True, blank=True)
    amount = models.CharField(max_length=50, null=True, blank=True)
    business_shortcode = models.CharField(max_length=50, null=True, blank=True)
    account_no = models.CharField(max_length=100, null=True, blank=True)
    invoice_no = models.CharField(max_length=100, null=True, blank=True)
    org_acc_balance = models.CharField(max_length=100, null=True, blank=True)
    thirdparty_trans_id = models.CharField(max_length=100, null=True, blank=True)
    phonenumber = models.CharField(max_length=15, null=True, blank=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"C2B Transaction {self.transaction_id}"


class MpesaB2C(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='mpesa_b2cs', null=True)
    page = models.ForeignKey('mchango.ContributionPage', on_delete=models.CASCADE, related_name='mpesa_b2cs', null=True)
    conversation_id = models.CharField(max_length=100)
    originator_conversation_id = models.CharField(max_length=100)
    trans_id = models.CharField(max_length=100, null=True, blank=True)
    result_parameters = models.JSONField(null=True, blank=True)
    status = models.ForeignKey('mchango.Status', on_delete=models.CASCADE, related_name='mpesa_b2cs', null=True)
    result_type = models.CharField(max_length=100, null=True, blank=True)
    result_code = models.CharField(max_length=50, null=True, blank=True)
    result_desc = models.CharField(max_length=255, null=True, blank=True)
    trans_amount = models.CharField(max_length=50, null=True, blank=True)
    registered_customer = models.CharField(max_length=50, null=True, blank=True)
    receiver_party_public_name = models.CharField(max_length=255, null=True, blank=True)
    b2c_charges_paid_account_available_funds = models.CharField(max_length=100, null=True, blank=True)
    b2c_utility_account_available_funds = models.CharField(max_length=100, null=True, blank=True)
    b2c_working_account_available_funds = models.CharField(max_length=100, null=True, blank=True)
    trans_date = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"B2C Transaction {self.transaction_id}"
