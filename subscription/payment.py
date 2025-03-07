import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import json
from .models import Subscription
from plan.models import Plan
from business.models import Business
from django.conf import settings

def initialize_paystack_transaction(email, amount, business, plan):
    print(str(business) + " " + str(plan))
    url = "https://api.paystack.co/transaction/initialize"
    
    headers = {
        "Authorization": f"Bearer sk_test_924f1f3e749ba7247e947e1b882de7d60d4a6019",
        "Content-Type": "application/json"
    }
    
    data = {
        "email": email,
        "amount": int(amount * 100),
        "reference": f"subscription.{business}.{plan}",
        "metadata": {
            "business": str(business),
            "plan": str(plan)
        }
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # Raise HTTP errors (4xx, 5xx)
        response_data = response.json()
        
        # Return the payment link if request is successful
        return response_data.get("data", {}).get("authorization_url")
    
    except requests.exceptions.RequestException as e:
        print(f"Paystack API error: {e}")  # Log error
        return None  



@method_decorator(csrf_exempt, name='dispatch')
class PaystackWebhookView(View):
    def post(self, request, *args, **kwargs):
        try:
            event = json.loads(request.body)
            event_type = event.get('event')
            print("event_type:", event_type)

            if event_type == 'charge.success':
                # Get transaction reference
                data = event.get('data', {})
                reference = data.get('reference')

                # Find the subscription
                try:
                    subscription = Subscription.objects.get(reference=reference)
                except Subscription.DoesNotExist:
                    return JsonResponse({'status': 'error', 'message': 'Subscription not found'}, status=404)

                # Get the related business and plan
                plan = subscription.plan  # Assuming it's a ForeignKey
                business = subscription.business  # Assuming it's a ForeignKey

                # Update business plan if applicable
                business.plan = plan.name
                business.save()

                # Update subscription status
                subscription.status = 'ACTIVE'
                subscription.payment_status = 'PAID'
                subscription.save()

                return JsonResponse({'status': 'success'}, status=200)
            else:
                return JsonResponse({'status': 'ignored'}, status=200)
        
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)