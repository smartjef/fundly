from django import forms
from .models import ContributionPage, Pledge

class ContributionPageForm(forms.ModelForm):
    class Meta:
        model = ContributionPage
        fields = ['photo', 'purpose', 'target', 'deadline', 'note']
        widgets = {
            'deadline': forms.DateTimeInput(attrs={'type': 'date'})
        }

class PledgeForm(forms.ModelForm):
    class Meta:
        model = Pledge
        fields = ['amount', 'to_pay_by']
        widgets = {
            'to_pay_by': forms.DateTimeInput(attrs={'type': 'date'})
        }
        