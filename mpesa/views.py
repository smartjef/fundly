from django.shortcuts import render
from django.contrib.auth.models import User
from mchango.models import ContributionPage, Transaction, Pledge
from mpesa.models import MpesaC2B
from decimal import Decimal
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def b2c_result(request):
    """Handles B2C transaction result and prints received data"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print("\n=== B2C RESULT RECEIVED ===")
            print(json.dumps(data, indent=4))  # Pretty print JSON for debugging

            return JsonResponse({"message": "B2C result received successfully"}, status=200)
        except Exception as e:
            print(f"Error processing B2C result: {e}")
            return JsonResponse({"error": str(e)}, status=400)

@csrf_exempt
def b2c_timeout(request):
    """Handles B2C timeout response and prints received data"""
    print("\n=== B2C TIMEOUT RECEIVED ===")
    print(request.body.decode('utf-8'))  # Print raw request body
    return JsonResponse({"message": "B2C timeout received"}, status=200)

@csrf_exempt
def c2b_confirm(request):
    """Handles C2B confirmation and prints received data"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print("\n=== C2B CONFIRMATION RECEIVED ===")
            print(json.dumps(data, indent=4))

            account_no = data.get("BillRefNumber", "").strip()

            # Initialize user, page, and pledge as None
            user = None
            page = None
            pledge = None

            parts = account_no.split("#")

            if len(parts) == 1:
                account_no = parts[0]
            elif len(parts) == 2:
                account_no, user_id = parts
                try:
                    user = User.objects.get(id=user_id)
                except User.DoesNotExist:
                    print(f"User with ID {user_id} not found")
            elif len(parts) == 3:
                account_no, user_id, pledge_id = parts
                try:
                    user = User.objects.get(id=user_id)
                except User.DoesNotExist:
                    print(f"User with ID {user_id} not found")
                
                try:
                    pledge = Pledge.objects.get(id=pledge_id)
                except Pledge.DoesNotExist:
                    print(f"Pledge with ID {pledge_id} not found")

            # Try to get the page
            try:
                page = ContributionPage.objects.get(account_no=account_no)
            except ContributionPage.DoesNotExist:
                print(f"Contribution Page with ID {account_no} not found")

            # If no user and no page, do not save the transaction
            if not user and not page:
                print("Neither user nor page found. Skipping transaction save.")
                return JsonResponse({"message": "No valid page or user found. Transaction skipped."}, status=400)

            # Save transaction
            MpesaC2B.objects.create(
                user=user,
                page=page,
                trans_type=data.get("TransactionType"),
                trans_id=data.get("TransID"),
                amount=data.get("TransAmount"),
                business_shortcode=data.get("BusinessShortCode"),
                account_no=account_no,
                invoice_no=data.get("InvoiceNumber"),
                org_acc_balance=data.get("OrgAccountBalance"),
                thirdparty_trans_id=data.get("ThirdPartyTransID"),
                phonenumber=data.get("MSISDN"),
                first_name=data.get("FirstName"),
            )

            # Fetch the last transaction safely
            last_transaction = Transaction.objects.last()
            last_org_balance = Decimal(last_transaction.org_balance) if last_transaction else Decimal(0)

            # Add new transaction amount
            org_balance = last_org_balance + Decimal(data.get("TransAmount"))

            if pledge:
                pledge.balance = pledge.balance - Decimal(data.get("TransAmount", "0"))
                pledge.save()

            # Handle page balance
            if page:
                last_page_transaction = page.transactions.last()
                last_pg_balance = Decimal(last_page_transaction.pg_balance) if last_page_transaction else Decimal(0)
                pg_balance = last_pg_balance + Decimal(data.get("TransAmount"))

            phone_number = data.get("MSISDN")
            if user and user.profile.phone_number:
                phone_number = user.profile.phone_number

            #save transaction
            trans = Transaction.objects.create(
                user = user,
                phone = phone_number,
                mpesa_ref_id = data.get('TransID'),
                date = data.get('TransTime'),
                amount = data.get('TransAmount'),
                org_balance = org_balance,
                pg_balance = pg_balance,
                page = page,
                pledge = pledge,
                first_name = data.get("FirstName"),
                meta = data
            )

            trans.save()

            print("Transaction saved successfully!")

            return JsonResponse({"message": "C2B confirmation received"}, status=200)
        except Exception as e:
            print(f"Error processing C2B confirmation: {e}")
            return JsonResponse({"error": str(e)}, status=400)
