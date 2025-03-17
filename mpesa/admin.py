from django.contrib import admin
from .models import MpesaB2C, MpesaC2B, MpesaSTK
# Register your models here.

@admin.register(MpesaB2C)
class MpesaB2CAdmin(admin.ModelAdmin):
    list_display = ['user', 'page', 'result_type', 'trans_id', 'status', 'result_code', 'trans_amount', 'registered_customer', 'receiver_party_public_name']
    list_filter = ['user', 'page', 'status', 'created_at', 'updated_at']
    search_fields = ['result_code', 'registered_customer', 'result_desc', 'status_name']
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    list_per_page = 20

@admin.register(MpesaC2B)
class MpesaC2BAdmin(admin.ModelAdmin):
    list_display = ['user', 'page', 'trans_type', 'trans_id', 'account_no', 'first_name', 'amount', 'business_shortcode']
    list_filter = ['user', 'page', 'created_at', 'updated_at']
    search_fields = ['trans_id', 'amount', 'account_no']
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    list_per_page = 20

@admin.register(MpesaSTK)
class MpesaSTKAdmin(admin.ModelAdmin):
    list_display = ['user', 'page', 'trans_id', 'result_code', 'result_desc', 'amount', 'trans_date']
    list_filter = ['user', 'page', 'created_at', 'updated_at']
    search_fields = ['trans_id', 'result_desc', 'amount']
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    list_per_page = 20