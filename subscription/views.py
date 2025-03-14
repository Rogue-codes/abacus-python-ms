from django.shortcuts import render
from django.shortcuts import render
from rest_framework import status, generics, serializers
from .serializer import CreateSubscriptionSerializer
from rest_framework.response import Response
from django.utils.timezone import now 
from plan.models import Plan
from business.models import Business
from .payment import initialize_paystack_transaction
from dateutil.relativedelta import relativedelta
from .models import Subscription


# Create your views here.
class CreateSubscriptionView(generics.CreateAPIView):
    serializer_class = CreateSubscriptionSerializer

    def perform_create(self, serializer):
        plan_id = self.request.data.get('plan')
        business_email = self.request.data.get('business_email')
        cycle = self.request.data.get('cycle', 'MONTHLY') 

        expiry_date = now()
        if cycle == "YEARLY":
            expiry_date += relativedelta(years= 1)
        else:
            expiry_date += relativedelta(months= 1)

        try:
            plan = Plan.objects.get(id=plan_id)
            business = Business.objects.get(email=business_email)
            if not business.is_verified and not business.is_active:
                raise serializers.ValidationError({"business": "Business is not verified or active."})
        except Plan.DoesNotExist:
            raise serializers.ValidationError({"plan": "Plan does not exist."})
        except Business.DoesNotExist:
            raise serializers.ValidationError({"business": "Business does not exist."})

        # Calculate amount based on cycle
        amount = plan.price * 12 if cycle == "YEARLY" else plan.price

        already_existing_subscription = Subscription.objects.filter(business_id=business.id).first()

        if already_existing_subscription and already_existing_subscription.status == "ACTIVE":
            raise Exception("This business already has an active subscription")
        
        # Save subscription with required fields
        subscription = serializer.save(business=business, plan=plan, amount=amount, expiry_date=expiry_date)

        business = subscription.business
        # Update business plan if applicable
        business.plan = plan
        business.save()

        # Initialize payment
        self.payment_url=initialize_paystack_transaction(business.email, amount, business.id, plan.id)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response(
            {
                "success": True,
                "message": "Subscription created successfully",
                "data": response.data,
                "payment_link": self.payment_url,
            },
            status=status.HTTP_201_CREATED,
        )
