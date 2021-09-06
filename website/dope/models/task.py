from django.db import models
from dope.models.item import Item
from django.contrib.auth.models import User

from payments.models import Coupon
from .gateway import Suffix
from .accounts import FootLockerAccount


class Task(models.Model):
    """
    Bot Task

    user - Related User
    coupon - If user use a coupon | exist only if active == True
    active - Bool field check if task is activate
    gateway - (Suffix) Website related
    item - Product to buy
    account - Website Account used
    """
    PENDING = "pending"
    INPROGRESS = "inprogress"
    SUCCESS = "success"
    FAILED = "failed"

    STATES_CHOICES = (
        (PENDING, "Pending"),
        (INPROGRESS, "In Progress"),
        (SUCCESS, "Success"),
        (FAILED, "Failed")
    )

    user = models.ForeignKey(User, related_name='tasks', blank=False, on_delete=models.CASCADE)
    coupon = models.OneToOneField(Coupon, related_name='tasks', on_delete=models.DO_NOTHING, blank=True, null=True) # When active == True
    state:bool = models.CharField(choices=STATES_CHOICES, default=PENDING, max_length=10)
    date = models.DateTimeField(blank=False)

    gateway = models.ForeignKey(Suffix, related_name='tasks', blank=False, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, related_name='tasks', blank=False, on_delete=models.DO_NOTHING)
    
    # Accounts:
    footLockerAccount = models.ForeignKey(FootLockerAccount, related_name='tasks', on_delete=models.CASCADE, blank=True, null=True)
    
    

    def __str__(self) -> str:
        return '{}:  {} | {} | {}. State: {}'.format(
            self.user, self.gateway, self.item, self.date, self.state)

    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Tasks"
        ordering = ['date',]

    