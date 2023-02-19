from django.contrib import admin
from .models import StripeModel, BillingAddress, OrderModel,User, Tweet, TweetLike, UserFollower


admin.site.register(StripeModel)
admin.site.register(BillingAddress)
admin.site.register(OrderModel)
admin.site.register(User)
admin.site.register(Tweet)
admin.site.register(TweetLike)
admin.site.register(UserFollower)