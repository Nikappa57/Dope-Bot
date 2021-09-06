from datetime import date, datetime

from django.contrib.auth.models import User
from django.db import models

from dope.models.gateway import Gateway
from dope.models.task import Task


class Permission(models.Model):
    """
    Permission

    createAt - Datetime auto
    lastModification - last modify for plan
    expireAt - When plan expire
    maxTasks - max task for the gateway in the same time

    gateway - Related Gateway
    user - Related User
    """ 
    creatAt = models.DateTimeField(auto_now_add=True)
    lastModification = models.DateTimeField(auto_now_add=True)
    expireAt = models.DateField(blank=False, null=False)
    maxTasks = models.IntegerField(blank=False, null=False)

    gateway = models.ForeignKey(Gateway, blank=False, null=False, related_name='permissions', on_delete=models.CASCADE)
    user = models.ForeignKey(User, blank=False, null=False, related_name='permissions', on_delete=models.CASCADE)


    @property
    def expired(self) -> bool:
        return self.expireAt < date.today()

    @property
    def canAddTask(self) -> bool:
        tasks = Task.objects.filter(
            user=self.user, 
            state__in=[Task.PENDING, Task.INPROGRESS], 
            gateway__in=self.gateway.suffixUrls.all()
        )
        
        return tasks.count() < self.maxTasks
    
    @property
    def hasMaxTasks(self) -> bool:
        return self.maxTasks >= self.gateway.maxTaskForAccount
            

    def __str__(self) -> str:
        return "{} - {}".format(self.gateway, self.user)

    class Meta:
        verbose_name = "Permission"
        verbose_name_plural = "Permissions"
        unique_together = ["user", "gateway"]



