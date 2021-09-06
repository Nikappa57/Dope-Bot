import functools

from django.shortcuts import get_object_or_404, redirect
from django.urls.base import reverse
from django.contrib import messages

from dope.models.gateway import Suffix, Gateway

from core.models.permission import Permission


def add_task_required(func):
    """
    Controlla se l'utente può aggiungere una nuova task
    
    gli args devono contenere: request, gatewaySlug:str

    restituisce gli args: request, gatewaySuffix:Suffix, gateway:Gateway
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        request = args[0]
        slug = kwargs.pop('gatewaySlug')

        gatewaySuffix:Suffix = get_object_or_404(Suffix, slug__iexact=slug)
        gateway = gatewaySuffix.gateway
        permission:Permission = Permission.objects.filter(user=request.user, gateway=gateway).first()
        
        if gateway.deactivate:
            messages.error(request, 'Questo Gateway non è momentaneamente disponibile')
            return redirect(reverse('panel_view'))
        
        if gatewaySuffix.deactivate:
            print(3)
            messages.error(request, 'Questo sito non è momentaneamente disponibile')
            return redirect(reverse('panel_view'))

        if not permission:
            # TODO: rimanda alla pagina per comprare
            messages.error(request, 'Non Hai il permesso')
            return redirect(reverse('panel_view'))

        if permission.expired:
            # TODO manda alla pagina per modificare il plan
            messages.error(request, 'Plan scaduto')
            return redirect(reverse('panel_view'))
        
        if not permission.canAddTask:
            # TODO manda alla pagina per modificare il plan
            messages.error(request, 'Hai ragiunto il limite massimo di task in coda, eliminane 1 o modifica il tuo plan')
            return redirect(reverse('panel_view'))

        
        kwargs["gatewaySuffix"] = gatewaySuffix
        kwargs["gateway"] = gateway

        value = func(*args, **kwargs)
        return value
    return wrapper