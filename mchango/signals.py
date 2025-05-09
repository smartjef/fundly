from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ContributionPage, Pledge, Transaction
from main.helper  import send_sms

@receiver(post_save, sender=ContributionPage)
def send_sms_on_status_change(sender, instance, **kwargs):
    """Sends an SMS when a ContributionPage status changes."""
    if instance.status.name in ['Active', 'Rejected', 'Closed']:
        phone_number = instance.user.profile.phone_number
        first_name = instance.user.first_name
        if phone_number and first_name:
            message = f"Dear {instance.user.first_name}, your campaign page has been {instance.status}."
            send_sms(phone_number, message)
        else:
            print("Phone number or first name is missing. SMS not sent.")
    else:
        print("SMS not sent. Status change not applicable.")

@receiver(post_save, sender=Pledge)
def send_sms_on_pledge_creation(sender, instance, created, **kwargs):
    """Sends an SMS when a new Pledge is created."""
    if created:
        pledger_phone = instance.user.profile.phone_number
        owner_phone = instance.page.user.profile.phone_number
        pledger_name = instance.user.first_name
        owner_name = instance.page.user.first_name

        if pledger_phone and pledger_name:
            message_pledger = f"Dear {pledger_name}, Your pledge of Ksh. {instance.amount}(ID: {instance.id}) has been recorded successfully! Kindly honor it by {instance.to_pay_by}. Thank you in advance!\nRegards,\n{owner_name}\n"
            send_sms(pledger_phone, message_pledger)

        if owner_phone and owner_name:
            message_owner = f"Dear {owner_name}, {pledger_name} has pledged Ksh. {instance.amount} to be paid by {instance.to_pay_by}."
            send_sms(owner_phone, message_owner)

@receiver(post_save, sender=Transaction)
def send_sms_on_pledge_creation(sender, instance, created, **kwargs):
    """Sends an SMS when a new Transaction is created."""
    if created and instance.trans_type == 'Contribution':
        phone = instance.phone
        owner_phone = instance.page.user.profile.phone_number
        name = instance.user.first_name
        owner_name = instance.page.user.first_name

        if phone and name:
            message = f"Dear {name}, Thank you for your contribution. Well Received!\nRegards,\n{owner_name}\n"
            send_sms(phone, message)

        if owner_phone and owner_name:
            message_owner = f"Dear {owner_name}, You've received {name}'s contribution of Ksh. {instance.amount}. MPESA Ref: {instance.mpesa_ref_id}. Balance: Ksh {instance.page.get_total_contributions() or 0}"
            send_sms(owner_phone, message_owner)
    else:
        print("SMS not sent. Transaction Type is not applicable.")
