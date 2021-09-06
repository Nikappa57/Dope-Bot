from django.contrib import admin

from .models.pricing import Pricing
from .models.coupon import Coupon


admin.site.register(Coupon)
admin.site.register(Pricing)