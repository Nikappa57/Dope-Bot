from django.db import models
from django.contrib.auth.models import User

from dope.models.gateway import Gateway


class Coupon(models.Model):
    """
    One Time Coupon
    
    user - ForeignKey User (django.contrib.auth.models)
    gateway - Gateway Supported (ForeignKey)
    expire_at - Expire Date (1 year later)
    name - Random name 
    """
    user = models.ForeignKey(User, related_name='coupons', blank=False, on_delete=models.CASCADE)
    gateway = models.ForeignKey(Gateway, related_name='coupons', blank=False, on_delete=models.CASCADE)
    expire_at = models.DateTimeField(blank=False) # default=datetime.now() + timedelta(days=365)
    name:str = models.CharField(max_length=10, blank=False)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Coupon"
        verbose_name_plural = "Coupons"

