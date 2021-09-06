from datetime import date, datetime, timedelta
import re

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http.response import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls.base import reverse

from payments.forms import genDetailsPlanForm, genGatewayPlanForm
from dope.models.gateway import Gateway
from core.models.permission import Permission


@login_required
def chooseGatewayPlan(request):
    excludedGateways = [p.gateway for p in request.user.permissions.all()]

    if len(excludedGateways) == len(Gateway.objects.all()):
        messages.error(request, "You just have all gateways in your Plan.")
        return redirect(reverse('profile_view'))

    if request.method == "POST":
        form = genGatewayPlanForm(request=request.POST, excludedGateways=excludedGateways)
        if form.is_valid():
            return redirect(
                reverse('choose_details_plan', 
                args=["-".join(form.cleaned_data["gateways"])])
            )
    else:
        form = genGatewayPlanForm(excludedGateways=excludedGateways)

    title = 'Create your Plan' if not excludedGateways else 'Add new Gateways to your Plan'
    context = {'form': form, 'title': title}

    # TODO: Nel file html: Controllare come mettere dinamico il link, modificare tutto in jquery.
    return render(request, "payments/plan-create-mofify.html", context)


@login_required
def chooseDetailsPlan(request, gateways:str):
    
    PATTERN = "^[A-Za-z]+(-[A-Za-z]+)*$"
    if not re.match(PATTERN, gateways):
        raise Http404("Invalid gateway")

    gateways = gateways.split("-")
    
    for name in gateways:
        gatewayQuerySet = Gateway.objects.filter(name=name)
        if not gatewayQuerySet.exists():
            return Http404("Gateway not exist")
        
        permissionQuerySet = Permission.objects.filter(user=request.user, gateway=gatewayQuerySet.first())
        if permissionQuerySet.exists():
            return Http404("your plan already have {} in gateways list".format(
                gatewayQuerySet.first().name))

    if request.method == "POST":
        form = genDetailsPlanForm(gateways, request=request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            # TODO: pagamento
            data = list(form.cleaned_data.values())
            details = [[data[i], data[i + 1]] for i in range(0, len(data), 2)]

            for i, details in enumerate(details):
                gateway = Gateway.objects.filter(name=gateways[i]).first()
                month, tasks = details
                new_perm = Permission(
                    user=request.user, 
                    gateway=gateway,
                    expireAt=date.today() + timedelta(days=30 * int(month)),
                    maxTasks=tasks,
                    )
                new_perm.save()

            messages.success(request, "Plan added successfully.")
            return redirect(reverse('profile_view'))
    else:
        form = genDetailsPlanForm(gateways)

    context = {'form': form, 'title': 'Choose Details', "showPrice": True}
    return render(request, "payments/plan-create-mofify.html", context)


@login_required
def modifyDetailsPlan(request, permissionId:int):
    permission = get_object_or_404(Permission, id=permissionId)

    if permission.expired:
        messages.error(request, "You can't modify an expired Plan.")
        return redirect(reverse('profile_view'))
    
    if permission.hasMaxTasks:
        messages.error(request, "your plan already has the maximum of tasks available.")
        return redirect(reverse('profile_view'))

    if request.method == "POST":
        form = genDetailsPlanForm(
            gateways=[permission.gateway.name], 
            timeField=False, 
            minTasksValue=permission.maxTasks,
            request=request.POST,
        )
        if form.is_valid():
            permission.maxTasks = form.cleaned_data["{}-tasks".format(permission.gateway.name)]
            permission.lastModification = datetime.now()
            permission.save()

            messages.success(request, "Plan modified successfully")
            return redirect(reverse('profile_view'))
    else:
        form = genDetailsPlanForm(
            gateways=[permission.gateway.name], 
            timeField=False,
            minTasksValue=permission.maxTasks,
        )

    context = {'form': form, 'title': 'Modify Your Plan', "showPrice": True}

    return render(request, "payments/plan-create-mofify.html", context)


@login_required
def renewPlan(request, permissionId:int):
    permission = get_object_or_404(Permission, id=permissionId)

    if not permission.expired:
        messages.error(request, "You plan is not expired.")
        return redirect(reverse('profile_view'))

    if request.method == "POST":
        form = genDetailsPlanForm(
            gateways=[permission.gateway.name], 
            initalTasks=permission.maxTasks,
            request=request.POST,
        )
        if form.is_valid():
            # TODO: pagamento
            tasks = form.cleaned_data["{}-tasks".format(permission.gateway.name)]
            month = form.cleaned_data["{}-time".format(permission.gateway.name)]

            permission.maxTasks = tasks
            permission.expireAt = date.today() + timedelta(days=30 * int(month))
            permission.lastModification = datetime.now()
            permission.save()

            messages.success(request, "Plan renewed successfully")
            return redirect(reverse('profile_view'))
    else:
        form = genDetailsPlanForm(
            gateways=[permission.gateway.name],
            initalTasks=permission.maxTasks,
        )
        
    context = {'form': form, 'title': 'Renew your Plan'}
    return render(request, "payments/plan-create-mofify.html", context)