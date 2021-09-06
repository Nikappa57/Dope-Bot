from typing import Dict

from django.db import models
from django.db.models.query import QuerySet
from django.db.models.signals import pre_save
from django.dispatch import receiver

from SneakersBot.utils import unique_slug_generator
from dope.models.paymentMethod import PaymentMethod


class Gateway(models.Model):
    """ 
    List of supported Website

    name - Name of gateway
    prefixUrl - Website url start
    paymentMethods - Payments method supported
    supportedAccount - Account supported by Gateway
    deactivate - if admin wont to deative gateway (for coming soon or maintenance)
    (coupons) - Coupon (optional)

    stock - max plan buyable
    (price) - price based on time
    priceForTask - price based on maxtask
    """

    FOOTLOCKER = "FootLocker" 
    NIKE = "Nike"

    NAMES_CHOICES = (
        (FOOTLOCKER, FOOTLOCKER),
        (NIKE, NIKE)
    )

    name:str = models.CharField(max_length=40, choices=NAMES_CHOICES, blank=False, unique=True) 
    prefixUrl:str = models.CharField(max_length=125, blank=False, unique=True)
    supportedAccount:str = models.CharField(max_length=125, blank=True, null=True)
    deactivate:bool = models.BooleanField(default=False)

    maxTaskForAccount:int = models.IntegerField(default=10)

    # Pricing
    stock:int = models.IntegerField(null=True, blank=True)
    priceForTask:float = models.FloatField(null=True, blank=True)

    paymentMethods:QuerySet[PaymentMethod] = models.ManyToManyField(PaymentMethod, related_name='gateways', blank=False)

    def __str__(self) -> str:
        return self.name

    @staticmethod
    def getAllUrls() -> Dict[str, Dict[str, str]]:
        gateways = Gateway.objects.all()
        urls = {
            gateway.name: {
                suffix.name: 
                    suffix.slug if not gateway.deactivate and not suffix.deactivate else None
                    for suffix in gateway.suffixUrls.all()
            } for gateway in gateways
        }
        print(urls)

        return urls

    class Meta:
        verbose_name = "Gateway"
        verbose_name_plural = "Gateways"
        ordering = ['name']



class Suffix(models.Model):
    """ 
    List of suffix url Website

    name - Name of suffix (ex: .it, .fr...)
    suffix - str
    slug - SlugField
    deactive - true if suffix is deactive

    (gateways) - related Gateway
    (tasks) - Bot Task
    """

    name:str = models.CharField(max_length=40, blank=False, unique=True)
    suffixUrl:str = models.CharField(max_length=125, blank=False)
    deactivate:bool = models.BooleanField(default=False)
    slug:str = models.SlugField(max_length=250, null=True, blank=True)

    gateway:Gateway = models.ForeignKey(Gateway, related_name='suffixUrls', on_delete=models.CASCADE)

    @property
    def url(self) -> str:
        return self.gateway.prefixUrl + self.suffixUrl

    def __str__(self) -> str:
        return self.name
    

    
    class Meta:
        verbose_name = "Suffix"
        verbose_name_plural = "Suffixes"
        ordering = ['name']

@receiver(pre_save, sender=Suffix)
def pre_save_receiver(sender, instance, *args, **kwargs):
    instance.slug = unique_slug_generator(instance)
       