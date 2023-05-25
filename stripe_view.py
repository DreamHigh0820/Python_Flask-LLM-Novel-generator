from datetime import datetime
import stripe
import os
from flask import Blueprint, request, jsonify, redirect, url_for
from models import User, Fingerprints
from flask_login import current_user,login_required

stripe_view = Blueprint('stripe_view',__name__)

TOKENS = {
  499:["price_1N2qB5A3PenN3g4BeyJ9H3yH",250],
  1999:["price_1N2fgDA3PenN3g4BpBmLWqho",1_200],
  4999:["price_1N2fgxA3PenN3g4BqrMEOeTV",3_500],
  9999:["price_1N2fhtA3PenN3g4Be8cvggGV",8_000]
}
TIERS = {
    'FREE':['price_1N2abtA3PenN3g4BzMaBwrTN',250],
    'BASIC':['price_1N2aZJA3PenN3g4BZafLWjmE',700],
    'PREMIUM':['price_1N2o3jA3PenN3g4BEaC388Vq',1_200],
    'ENTERPRISE':['price_1N2o3jA3PenN3g4BEaC388Vq',5_500],
}

stripe.api_key = os.environ.get('stripe')
endpoint_secret = "whsec_OwQMJpBYWb3YC5XbQ4eQYQ1nVSDIWmzm"

def add_customer(email,i):
    customer = stripe.Customer.create(
      name = f"customer {i}",
      email=email,
    )
    return customer["id"]

@stripe_view.route('/create-payment', methods=['POST'])
@login_required
def create_payment_checkout():
    token = request.form.get('token')
    try:
        token = int(token)
    except:
        return "Invalid Token!!"
    if token not in TOKENS.keys():
        return "Invalid Token!!"
    try:
        checkout_session = stripe.checkout.Session.create(
        customer=current_user.customer_id,
        payment_method_types=['card'],
        line_items=[{
            'price':TOKENS[token][0],
            'quantity': 1,
        }],
        mode="payment", #payment for single purchase or subscription
        success_url="https://aing-j2lus53e4q-uc.a.run.app/home",
        cancel_url="https://aing-j2lus53e4q-uc.a.run.app/home",
        )
        return redirect(checkout_session.url, code=303)
    except Exception as e:
        return jsonify({'error': {'message': str(e)}}), 400

@stripe_view.route('/create-subscription', methods=['POST'])
@login_required
def create_subscription_checkout():
    tier = request.form.get('tier')
    if tier == "NORMAL" and current_user.had_free_trial:
        #stop him because he already got free trial
        return ""
    if tier not in TIERS.keys():
        return "plan error"
    try:
        checkout_session = stripe.checkout.Session.create(
        customer=current_user.customer_id,
        payment_method_types=['card'],
        line_items=[{
            'price':TIERS[tier][0],
            'quantity': 1,
        }],
        mode="subscription", #payment for single purchase or subscription
        success_url="https://aing-j2lus53e4q-uc.a.run.app/home",
        cancel_url="https://aing-j2lus53e4q-uc.a.run.app/home",
        )
        return redirect(checkout_session.url, code=303)
    except Exception as e:
        return jsonify({'error': {'message': str(e)}}), 400

@stripe_view.route('/webhook', methods=['POST'])
def webhook():
    payload = request.data
    sig_header = request.headers['STRIPE_SIGNATURE']

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        raise e
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        raise e

    if event.type == "customer.subscription.deleted":
        deleted_sub = event.data.object
        user = User.query.filter_by(customer_id=deleted_sub['customer']).first()
        user.tier = "Free"
        user.update()

    if event.type == "customer.subscription.updated":
        update_sub = event.data.object
        user = User.query.filter_by(customer_id=update_sub['customer']).first()
        plan = update_sub["plan"]["id"]
        tier = get_keys_by_values(plan)
        subscription = stripe.Subscription.retrieve(update_sub["id"])
        payment_method = stripe.PaymentMethod.retrieve(subscription.default_payment_method)
        cardFingerprint = payment_method.card.fingerprint
        fingerprint = Fingerprints.query.filter_by(fingerprint=cardFingerprint).first()
        if user.had_free_trial and tier == "FREE":
            return jsonify(success=False),400
        if fingerprint:
            return jsonify(success=False),400
        if tier == "FREE":
            user.had_free_trial = True
            fingerprintObject = Fingerprints(fingerprint=cardFingerprint,used_for_free_trial=True)
            fingerprintObject.add()
        user.tier = tier
        user.tokens += TIERS[tier][1]
        user.update()

    # Handle the charge succeeded event
    if event.type == 'charge.succeeded':
        charge = event.data.object
        if charge.description is None:
          user = User.query.filter_by(customer_id=charge.customer).first()
          user.tokens += TOKENS[charge.amount]
          user.update()
    return jsonify(success=True)

@stripe_view.route('/create-customer-portal-session', methods=['POST'])
def customer_portal():
  # Authenticate your user.
  session = stripe.billing_portal.Session.create(
    customer=current_user.customer_id,
    return_url="https://aing-j2lus53e4q-uc.a.run.app/",
  )
  return redirect(session.url)

def get_keys_by_values(price_id):
  for key,listValue in TIERS.items():
    if listValue[0]==price_id:
      return key
