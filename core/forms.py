from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

PAYMENT_CHOICE =(
    ('S','Stripe'),
    ('P','PayPal'),
)

POWER_TYPES_CHOICES = (
    ('Z', "Zero Power"),
    ('B', "Bifocal Power"),
    ('S', "Single Power"),
)

LENSES_TYPES_CHOICES = (
    ('HC', "Regular"),
    ('AR', "Anti-Glare"),
    ('BB', "Blue Blocker"),
)
class CheckoutForm(forms.Form):
    shipping_street_address = forms.CharField(required=False)
    shipping_apartment_address = forms.CharField(required=False)
    shipping_country = CountryField(blank_label='(Select Country)').formfield(
        required=False,
        widget=CountrySelectWidget(
           attrs={"class": "custom-select d-block w-100"}
        )
    )
    shipping_zip_code = forms.CharField(required=False)
    save_info = forms.BooleanField(widget=forms.CheckboxInput(),required=False)
    use_default_shipping = forms.BooleanField(widget=forms.CheckboxInput(),required=False)
    set_default_shipping = forms.BooleanField(widget=forms.CheckboxInput(),required=False)
    payment_method = forms.ChoiceField(widget=forms.RadioSelect(), choices=PAYMENT_CHOICE)


class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        'class':"form-control",
        'placeholder':'Promo Code',
        'aria-label':"Recipient's username",
        'aria-describedby':"basic-addon2"
    }))

class LensesForm(forms.Form):
    power_type = forms.ChoiceField(widget=forms.Select(
        attrs={
            "class": "custom-select d-block w-100",
            "id": "power_type",
        }
    ), choices=POWER_TYPES_CHOICES)

    lenses_type = forms.ChoiceField(widget=forms.Select(
        attrs={
            "class": "custom-select d-block w-100",
            "id": "lenses_type",
        }), choices=LENSES_TYPES_CHOICES)


    prescription_image = forms.ImageField()

class StripePaymentForm(forms.Form):
    stripeToken = forms.CharField(required=False)
    save = forms.BooleanField(required=False)
    use_default = forms.BooleanField(required=False)


class RefundForm(forms.Form):
    email = forms.EmailField(required=True)
    message = forms.CharField(required=True, widget = forms.Textarea(
        attrs={
            'rows': 4,
        }
    ))
    ref_code = forms.CharField(required=True)
