from django.db import models

from dope.models.gateway import Gateway


class Pricing(models.Model):
    """ 
    Pricing

    name - Name 
    description - description

    price - price
    month - month for this price
    gateway - Related Gateway
    """

    name:str = models.CharField(max_length=40, blank=False, null=False)
    description:str = models.TextField(blank=False, null=False)
    
    price:float = models.FloatField(null=False, blank=False)
    month:int = models.IntegerField(null=False, blank=False)
    gateway:Gateway = models.ForeignKey(Gateway, related_name="pricing", on_delete=models.CASCADE, null=False, blank=False)
    
    
    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Pricing"
        verbose_name_plural = "Pricing"
        ordering = ['gateway']
        unique_together = ["month", "gateway"]