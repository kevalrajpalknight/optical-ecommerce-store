from django.conf import settings
from django.db import models
from django.shortcuts import reverse
from django_countries.fields import CountryField
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver

CATEGORIES_CHOICES = (
    ('FS', "Full Sheet Frame"),
    ('FM', "Full Metal Frame"),
    ('3P', "Without Frame"),
    ('SP', "Half Frame"),
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

LABEL_CHOICES = (
    ('P', "primary"),
    ('S', "secondary"),
    ('D', "danger"),
)


ADDRESS_CHOICES = (
    ('B', "Billing"),
    ('S', "Shipping"),
)


# Create your models here.
class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    category = models.CharField(max_length=2, choices=CATEGORIES_CHOICES)
    label = models.CharField(max_length=1, choices=LABEL_CHOICES)
    slug = models.SlugField()
    description = models.TextField(default="This is a description of the product.")
    features = models.TextField(default="This is a description of the product.")
    fview = models.ImageField(upload_to="media/Item/", blank=True, null=True)
    sview = models.ImageField(upload_to="media/Item/", blank=True, null=True)

    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        return reverse("core:product-detail", kwargs={
            "slug":self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("core:add_to_cart", kwargs={
            "slug":self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("core:remove_from_cart", kwargs={
            "slug":self.slug
        })

class OrderItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    lenses_required = models.BooleanField(default=False)
    lenses = models.ForeignKey('EyeLenses', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return self.quantity * self.item.price
        
    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price
        
    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        else:
            return self.get_total_item_price()        

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    ordered = models.BooleanField(default=False)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    order_date = models.DateTimeField()
    shipping_address = models.ForeignKey('Address', related_name='shipping_address', on_delete=models.SET_NULL, null=True, blank=True)
    coupon = models.ForeignKey('Coupon', on_delete=models.SET_NULL, null=True, blank=True)

    failed_confirm = models.BooleanField(default=False)
    remark_for_failure = models.TextField(default="Please Contact to the store.")
    in_process_delivery = models.BooleanField(default=False)

    delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)

    refund_request = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)
    payment = models.ForeignKey('Payment', on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return str(self.user.username)

    def get_total_bill_amount(self):
        total_amount = 0
        for item in self.items.all():
            total_amount += item.get_final_price()
        return total_amount
        
    def get_total_bill_amount_with_discount(self):
        total_amount = 0
        for item in self.items.all():
            total_amount += item.get_final_price()
        if self.coupon:
            total_amount -= total_amount * (self.coupon.percentage/100)
        return total_amount

class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip_code = models.CharField(max_length=10)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)
    

    class Meta:
        verbose_name_plural = 'Addresses'

    def __str__(self):
        return self.user.username

class Payment(models.Model):
    transaction_id = models.CharField(max_length=100)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    time_stamp = models.DateTimeField(auto_now_add=True)
    amount = models.FloatField()
    def __str__(self):
        return f"$ {self.amount} bill of {self.user.username}"

class Coupon(models.Model):
    code = models.CharField(max_length=50)
    percentage = models.FloatField(default=0)
    def __str__(self):
        return self.code

class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    email = models.EmailField()
    message = models.TextField()
    accepted = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.pk}"

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    profile_image = models.ImageField(blank=True, null=True)
    phone = models.CharField(max_length=10,blank=True, null=True)

    def __str__(self):
        return self.user.username

class EyeLenses(models.Model):
    power_type = models.CharField(blank=True, null=True, max_length=1, choices=POWER_TYPES_CHOICES)
    lenses_type = models.CharField(blank=True, null=True, max_length=2, choices=LENSES_TYPES_CHOICES)
    prescription_image = models.ImageField(upload_to = "user_prescription/", blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

