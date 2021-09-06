from core.models.permission import Permission
from django.shortcuts import get_object_or_404

from dope.models.gateway import Gateway
from payments.models.pricing import Pricing


def getPriceOfPlan(user, gateway:Gateway, tasks:int=0, month:int=None) -> float:
    """
    Calcola il prezzo del plan in base al gateway, tasks e month
    
    se month è None/0, calcola il prezzo per la sola aggiunta delle tasks"""
    
    basePrice:float = get_object_or_404(Pricing, 
        month=month, gateway=gateway).price if month else 0

    permissionQuerySets = Permission.objects.filter(user=user, gateway=gateway)
    if permissionQuerySets.exists():
        tasks -= permissionQuerySets.first().maxTasks
        
    print("Base:", basePrice)
    print("TASKS:", tasks, "TASKS PRICE:", tasks * gateway.priceForTask)
    return round(basePrice + tasks * gateway.priceForTask, 2)