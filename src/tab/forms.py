from django import forms
from creditcards.forms import CardNumberField, CardExpiryField, SecurityCodeField

class PaymentForm(forms.Form):
    name_on_card = forms.CharField(max_length=50, required=True)
    cc_number = CardNumberField(label='Card Number')
    cc_expiry = CardExpiryField(label='Expiration Date')
    cc_code = SecurityCodeField(label='CVV/CVC')
