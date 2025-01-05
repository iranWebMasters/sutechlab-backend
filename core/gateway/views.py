import logging
from django.urls import reverse
from django.shortcuts import redirect, get_object_or_404
from azbankgateways import bankfactories, models as bank_models, default_settings as settings
from azbankgateways.exceptions import AZBankGatewaysException
from django.contrib import messages
from django.views import View
from orders.models import Order
from django.http import Http404
from .models import Payment


class GoToGatewayView(View):
    def get(self, request, payment_id):
        payment = get_object_or_404(Payment, id=payment_id)

        user_mobile_number = request.user.profile.phone_number if request.user.is_authenticated else None

        factory = bankfactories.BankFactory()
        try:
            bank = factory.auto_create()
            bank.set_request(request)
            bank.set_amount(payment.amount)
            print(payment.amount)
            # bank.set_client_callback_url(reverse('gateway:callback'))
            bank.set_client_callback_url(reverse('gateway:callback', kwargs={'payment_id': payment.id}))
            
            bank.set_mobile_number(user_mobile_number)

            bank_record = bank.ready()

            # Update the payment status to 'pending'
            payment.status = 'pending'
            payment.save()

            return bank.redirect_gateway()  # This should handle payment redirection
        except AZBankGatewaysException as e:
            logging.critical(e)
            messages.error(request, "اتصال به درگاه پرداخت ناموفق بود ، لطفا اتصال خود را به اینترنت بررسی نمایید و دوباره امتحان کنید")
            return redirect('userpanel:index')


class CallbackGatewayView(View):
    def get(self, request, payment_id):  # Add payment_id as a parameter
        tracking_code = request.GET.get(settings.TRACKING_CODE_QUERY_PARAM, None)
        if not tracking_code:
            logging.debug("این لینک معتبر نیست.")
            raise Http404("Invalid tracking code.")

        try:
            bank_record = bank_models.Bank.objects.get(tracking_code=tracking_code)
        except bank_models.Bank.DoesNotExist:
            logging.debug("این لینک معتبر نیست.")
            raise Http404("Invalid tracking code.")

        # Use the payment_id passed in the URL
        payment = get_object_or_404(Payment, id=payment_id)

        # Update the payment status based on the bank record's success
        if bank_record.is_success:
            payment.status = 'completed'


            # Update the laboratory request status
            order = payment.order
            order.status = 'successful'
            payment.tracking_code = tracking_code
            
            order.save()
            payment.save()

            messages.success(request, 'پرداخت با موفقیت انجام شد.')
            return redirect('userpanel:payment_success', tracking_code=tracking_code)  # Redirect to a success page
        else:
            payment.status = 'failed'
            payment.save()

            messages.error(request, 'پرداخت با شکست مواجه شده است. اگر پول از حساب کم شده است ظرف مدت ۴۸ ساعت پول به حساب شما بازخواهد گشت.')
            return redirect('userpanel:index')  # Redirect to the main page
