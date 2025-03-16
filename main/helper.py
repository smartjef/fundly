import os
import json
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Fetch secrets from .env
SENDER_ID = os.getenv("SENDER_ID")
API_KEY = os.getenv("API_KEY")
CLIENT_ID = os.getenv("CLIENT_ID")

def send_sms(phone_number, message_body):
    """
    Sends an SMS to a single recipient using Onfon Media API.
    
    :param phone_number: Recipient's phone number
    :param message_body: Message to send
    :return: Status of SMS sending
    """
    try:
        url = "https://api.onfonmedia.co.ke/v1/sms/SendBulkSMS"
        headers = {'Content-Type': 'application/json'}

        if not all([SENDER_ID, API_KEY, CLIENT_ID]):
            return "Missing API credentials in environment variables"

        payload = {
            'SenderId': SENDER_ID,
            'MessageParameters': [{'Number': phone_number, 'Text': message_body}],
            'ApiKey': API_KEY,
            'ClientId': CLIENT_ID
        }

        response = requests.post(url, data=json.dumps(payload), headers=headers)

        if response.status_code == 200:
            return f"SMS sent successfully to {phone_number}"
        else:
            return f"Failed to send SMS. Response: {response.status_code} - {response.text}"

    except Exception as e:
        return f"Error sending SMS: {e}"
