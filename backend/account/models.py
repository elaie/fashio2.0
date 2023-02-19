from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

class User(AbstractUser):
    display_name = models.CharField(max_length=255)
    verified = models.BooleanField(default=False)
    photo = models.URLField(blank=True)
    header_photo = models.URLField(blank=True)
    website = models.URLField(blank=True)
    bio = models.CharField(max_length=160, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=30, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    pass

class Tweet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=280)
    image = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class TweetLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='like_set')
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name='like_set')
    created_at = models.DateTimeField(auto_now_add=True)

class UserFollower(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    created_at = models.DateTimeField(auto_now_add=True)



# STRIPE MODEL
class StripeModel(models.Model):
    email = models.EmailField(null=True, blank=True)
    name_on_card = models.CharField(max_length=200, null=True, blank=True)
    customer_id = models.CharField(max_length=200, blank=True, null=True)
    card_number = models.CharField(max_length=16, unique=True, null=True, blank=True)
    exp_month = models.CharField(max_length=2, validators=[RegexValidator(r'^\d{0,9}$')], null=True, blank=True)
    exp_year = models.CharField(max_length=4, validators=[RegexValidator(r'^\d{0,9}$')], null=True, blank=True)
    card_id = models.TextField(max_length=100, null=True, blank=True)
    user = models.ForeignKey(User, related_name="stripemodel", on_delete=models.CASCADE, null=True, blank=True)
    address_city = models.CharField(max_length=120, null=True, blank=True)
    address_country = models.CharField(max_length=120, null=True, blank=True)
    address_state = models.CharField(max_length=120, null=True, blank=True)
    address_zip = models.CharField(max_length=6, validators=[RegexValidator(r'^\d{0,9}$')], null=True, blank=True)

    def __str__(self):
        return self.email


class BillingAddress(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    user = models.ForeignKey(User, related_name="billingmodel", on_delete=models.CASCADE, null=True, blank=True)
    phone_number = models.CharField(max_length=10, validators=[RegexValidator(r'^\+?1?\d{9,15}$')], null=False, blank=False)
    pin_code = models.CharField(max_length=6, validators=[RegexValidator(r'^\d{0,9}$')], null=False, blank=False)
    house_no = models.CharField(max_length=300, null=False, blank=False)
    landmark = models.CharField(max_length=120, null=False, blank=False)
    city = models.CharField(max_length=120, null=False, blank=False)
    state = models.CharField(max_length=120, null=False, blank=False)

    def __str__(self):
        return self.name


class OrderModel(models.Model):
    name = models.CharField(max_length=120)
    ordered_item = models.CharField(max_length=200, null=True, blank=True, default="Not Set")
    card_number = models.CharField(max_length=16, null=True, blank=True)
    address = models.CharField(max_length=300, null=True, blank=True)
    paid_status = models.BooleanField(default=False)
    paid_at = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    total_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    is_delivered = models.BooleanField(default=False)
    delivered_at = models.CharField(max_length=200, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) 