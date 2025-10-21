from django.urls import path
from .views import address, verify_code, payment

urlpatterns = [
    path('address/', address, name='login'),
    path('verify-code/', verify_code, name='verify_code'),
    path('payment/', payment, name='payment'),
]