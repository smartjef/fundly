from django.db import models
from django.utils import timezone
from django.urls import reverse
from decimal import Decimal
import uuid

class Status(models.Model):
    name = models.CharField(max_length=50)
    class_name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ('name',)
        get_latest_by = "created_at"


# Create your models here.
class ContributionPage(models.Model):
    photo = models.ImageField(upload_to='pages/%Y/', blank=True)
    purpose = models.TextField()
    target = models.DecimalField(max_digits=12, decimal_places=2)
    deadline = models.DateField()
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='pages')
    status = models.ForeignKey(Status, on_delete=models.CASCADE, related_name='pages')
    note = models.TextField(blank=True)
    account_no = models.CharField(max_length=20)
    slug = models.SlugField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Campaign {self.getId()}"
    
    def save(self, *args, **kwargs):
        # validate target
        if self.target < 500:
            raise ValueError('Target must be at least 500')
        # validate deadline
        
        if not self.pk:
            if self.deadline < timezone.now().date():
                raise ValueError('Deadline must be in the future')
            self.account_no = str(uuid.uuid4()).upper().replace('-', '')[:8]
            self.slug = str(uuid.uuid4()).lower().replace('-', '')
        super(ContributionPage, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('mchango:dashboard', args=[self.id,self.slug])
    
    def get_edit_url(self):
        return reverse('mchango:edit', args=[self.id,self.slug])
    
    def get_close_url(self):
        return reverse('mchango:close', args=[self.id,self.slug])
    
    def get_change_status_url(self):
        return reverse('mchango:change_status', args=[self.id,self.slug])
    
    def get_contribute_url(self):
        return reverse('mchango:contribute', args=[self.slug])
    
    def get_balance(self):
        return self.transactions.latest().pg_balance or 0;
    
    def get_total_contributions(self):
        return self.transactions.filter(trans_type='Contribution').aggregate(models.Sum('amount'))['amount__sum'] or 0
    
    def get_total_pledges(self):
        return self.pledges.aggregate(models.Sum('balance'))['balance__sum'] or 0
    
    def get_projection(self):
        return self.get_total_contributions() + self.get_total_pledges()
    
    def get_available_cash(self):
        return round(Decimal(0.98) * self.get_balance(),2)
    
    def get_progress(self):
        target = self.target
        balance = Decimal(self.get_total_contributions())
        return round((balance / target) * 100, 0) or 0
    
    def getId(self):
        return f"CP{str(self.id).zfill(4)}"
    
    def get_contributions(self):
        return self.transactions.filter(trans_type='Contribution')
    
    def get_pledges(self):
        return self.pledges.all().filter(balance__gt=0) 
    
    class Meta:
        ordering = ('-created_at', 'status')
        get_latest_by = "created_at"

# pledge
class Pledge(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='pledges')
    page = models.ForeignKey(ContributionPage, on_delete=models.CASCADE, related_name='pledges')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    to_pay_by = models.DateField()
    balance = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.first_name} pledges KES {self.amount}"
    
    def save(self, *args, **kwargs):
        if not self.pk:
            if self.to_pay_by < timezone.now().date():
                raise ValueError('To pay by must be in the future')
            self.balance = self.amount
        super(Pledge, self).save(*args, **kwargs)

    class Meta:
        ordering = ('-created_at',)
        get_latest_by = "created_at"
        unique_together = ('user', 'page')

class Transaction(models.Model):
    trans_type = models.CharField(max_length=50, choices=[('Contribution', 'Contribution'), ('Pledge', 'Pledge'), ('Withdrawal', 'Withdrawal'), ('Deposit', 'Deposit')], default='Contribution')
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='transactions', blank=True, null=True)
    phone = models.CharField(max_length=15)
    mpesa_ref_id = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    org_balance = models.DecimalField(max_digits=12, decimal_places=2)
    pg_balance = models.DecimalField(max_digits=12, decimal_places=2)
    page = models.ForeignKey(ContributionPage, on_delete=models.CASCADE, related_name='transactions')
    pledge = models.ForeignKey(Pledge, on_delete=models.CASCADE, related_name='transactions', blank=True, null=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    meta = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.trans_type}"
    
    def get_hidden_phone(self):
        phone = self.phone
        if phone.startswith('254'):
            return f"{phone[:4]}XX XXX {phone[-3:]}"
        elif phone.startswith('0'):
            return f"254{phone[1:3]} XX {phone[-3:]}"
        else:
            return phone

    class Meta:
        ordering = ('-created_at',)
        get_latest_by = "created_at"