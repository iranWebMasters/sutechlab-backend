import random
from django.apps import apps

def generate_order_code(customer_code):
    RequestInfo = apps.get_model('orders', 'RequestInfo')
    
    while True:
        random_number = random.randint(100, 999)
        order_code = f"{customer_code}-{random_number}"
        if not RequestInfo.objects.filter(order_code=order_code).exists():
            return order_code
