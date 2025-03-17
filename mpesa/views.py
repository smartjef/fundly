from django.shortcuts import render

# Create your views here.
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

            #save transaction to MPesaC2B model
            

            return JsonResponse({"message": "C2B confirmation received"}, status=200)
        except Exception as e:
            print(f"Error processing C2B confirmation: {e}")
            return JsonResponse({"error": str(e)}, status=400)
