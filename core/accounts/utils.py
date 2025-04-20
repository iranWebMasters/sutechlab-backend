from django.contrib.auth import get_user_model
import random
import string


def generate_unique_customer_code():
    User = get_user_model()
    prefix = ""
    while True:
        code = "".join(random.choices(string.digits, k=5))
        customer_code = f"{prefix}{code}"

        if not User.objects.filter(customer_code=customer_code).exists():
            return customer_code
