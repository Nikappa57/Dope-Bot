from payments.utils.pricing import getPriceOfPlan
from payments.decorators.restriction import private_view
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404

from dope.models.gateway import Gateway


@private_view
def getPriceOfPlanApi(request, gateway:str, tasks:int, month:int=None):
    print("ENTER")
    gateway:Gateway = get_object_or_404(Gateway, name=gateway)
    print("Gateway", gateway)
    price = getPriceOfPlan(request.user, gateway, tasks, month)
    print("Price", price)

    return JsonResponse({"price": price})