import sys

from django.db import models
from django.contrib.auth.models import User

from dope.models.gateway import Gateway

accountsModule = sys.modules[__name__]


class FootLockerAccount(models.Model):
    """
    Foot Locker Account 

    ... (TODO)
    gateway - Website Supported
    user - Related User
    (task) - list of Task 
    """ 
    GATEWAY = Gateway.FOOTLOCKER

    # TEST 
    name = models.CharField(max_length=30, blank=False)

    user = models.ForeignKey(User, blank=False, related_name='footlocker_accounts', on_delete=models.CASCADE)
    gateway = models.ForeignKey(Gateway, related_name='footlocker_accounts', blank=False, on_delete=models.CASCADE) # TODO: da avvisare l'utente

    def __str__(self) -> str:
        return 'FootLocker: {}'.format(self.name) # TODO

    class Meta:
        verbose_name = "FootLockerAccount"
        verbose_name_plural = "FootLockerAccounts"


# TEST
class NikeAccount(models.Model):
    """
    Nike (Snkrs) Account 

    ... (TODO)
    gateway - Website Supported
    user - Related User
    (task) - list of Task 
    """ 
    GATEWAY = Gateway.NIKE

    # TEST 
    name = models.CharField(max_length=30, blank=False)

    user = models.ForeignKey(User, blank=False, related_name='nike_accounts', on_delete=models.CASCADE)
    gateway = models.ForeignKey(Gateway, related_name='nike_accounts', blank=False, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return 'Nike: {}'.format(self.name) # TODO

    class Meta:
        verbose_name = "NikeAccount"
        verbose_name_plural = "NikeAccounts"