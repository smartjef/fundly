from django.contrib import admin
from .models import Status, ContributionPage, Pledge, Transaction
# Register your models here.


@admin.register(ContributionPage)
class ContributionPageAdmin(admin.ModelAdmin):
    list_display = ['target', 'deadline', 'user', 'status', 'account_no', 'slug', 'created_at', 'updated_at']
    list_filter = ['deadline', 'status', 'created_at', 'updated_at']
    search_fields = ['purpose', 'user_username', 'status_name']
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    list_per_page = 20

@admin.register(Pledge)
class PledgeAdmin(admin.ModelAdmin):
    list_display = ['user', 'page', 'amount', 'to_pay_by', 'balance', 'created_at', 'updated_at']
    list_filter = ['to_pay_by', 'created_at', 'updated_at']
    search_fields = ['user_username', 'page_purpose']
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    list_per_page = 20

@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ['name', 'class_name']
    search_fields = ['name', 'class_name']
    list_per_page = 20

@admin.register(Transaction)
class Transaction(admin.ModelAdmin):
    list_display = ['user', 'pledge', 'trans_type', 'amount', 'mpesa_ref_id', 'page', 'date', 'created_at']
    list_filter = ['date', 'created_at']
    search_fields = ['pledge_amount', 'mpesa_ref_id', 'page_purpose', 'user_username']
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    list_per_page = 20