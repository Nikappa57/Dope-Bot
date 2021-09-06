from django.db import models


class PaymentMethod(models.Model):
    """
    Payments method supported
    
    name - Name of method
    (gateways) - ManyToManyField -> Gateway
    pattern - regex pattern
    """

    name:str = models.CharField(max_length=25, blank=False)
    pattern:str = models.CharField(max_length=125, blank=False)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "PaymentMethod"
        verbose_name_plural = "PaymentMethods"
        ordering = ['name']
    