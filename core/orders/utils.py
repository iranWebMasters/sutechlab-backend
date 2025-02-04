import random
from django.apps import apps

def generate_order_code(customer_code):
    Order = apps.get_model('orders', 'Order')
    
    while True:
        random_number = random.randint(100, 999)
        order_code = int(f"{customer_code}"+f"{random_number}")
        if not Order.objects.filter(order_code=order_code).exists():
            return order_code
