from datetime import date, timedelta
from django.contrib.auth.decorators import login_required

from django.urls import reverse
from django.http import Http404
from django.core.paginator import Paginator
from django.views.generic.edit import UpdateView
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render

from dope.forms import genAccountForm
from dope.models import ACCOUNTS
from dope.models.gateway import Gateway
from dope.models.task import Task

@login_required
def panelView(request):
    expired = False
    if "expired" in request.GET.keys():
        if request.GET.get("expired") == "True":
            expired = True

    yesterday = (date.today() - timedelta(days=1)).strftime('%Y-%m-%d')

    tasks = request.user.tasks

    accounts = {
        modelName: {
            "accounts": ACCOUNTS[modelName].objects.filter(user=request.user),
            "gateway": ACCOUNTS[modelName].GATEWAY
        } for modelName in ACCOUNTS.keys() 
        if Gateway.objects.filter(name=ACCOUNTS[modelName].GATEWAY).exists()
    }

    if not tasks.exists():
        context = {
            'tasks': [], 
            'accounts': accounts, 
            "Task": Task, 
            "expired": expired,
        }

        return render(request, "dope/panel/panel.html", context)

    if expired:
        tasks_list = tasks.filter(
            date__range=["2021-01-01", yesterday])
    else:
        lastDate = tasks.last().date + timedelta(days=1)
        tasks_list = request.user.tasks.filter(
            date__range=[yesterday, lastDate.strftime('%Y-%m-%d')])

    
    paginator = Paginator(tasks_list, per_page=10)
    page = request.GET.get('page')
    
    if not page:
        page = 1
    
    tasks = paginator.get_page(page)

    context = {'tasks': tasks, 'accounts': accounts, "Task": Task, "expired": expired, "page": paginator.page(page)}

    return render(request, "dope/panel/panel.html", context)


@login_required
def addAccountView(request, gateway:str):
    gateway:Gateway = get_object_or_404(Gateway, name=gateway)

    if gateway.supportedAccount not in ACCOUNTS.keys():
        raise Http404('Account type not found')

    if request.method == "POST":
        form = genAccountForm(gateway.supportedAccount, request=request.POST)
        if form.is_valid():
            new_account = form.save(commit=False)
            new_account.user = request.user
            new_account.gateway = gateway
            
            new_account.save()
            next = request.GET.get('next')
            if next:
                return redirect(next)
            return redirect(reverse('panel_view'))
    else:
        form = genAccountForm(gateway.supportedAccount)

    context = {'form': form}

    return render(request, "dope/panel/newAccount.html", context)


@login_required
def editAccountView(request, gateway:str, accountId:int):
    gateway:Gateway = get_object_or_404(Gateway, name=gateway)

    if gateway.supportedAccount not in ACCOUNTS.keys():
        raise Http404('Account type not found')

    account = get_object_or_404(
            ACCOUNTS[gateway.supportedAccount], 
            id=accountId,
            user=request.user,
        )

    form = genAccountForm(gateway.supportedAccount, request=request.POST or None, instance=account)

    if request.method == "POST":
        if form.is_valid():
            new_account = form.save(commit=False)
            new_account.user = request.user
            new_account.gateway = gateway
            
            new_account.save()
            
            return redirect(reverse('panel_view'))

    context = {'form': form}
    
    return render(request, "dope/panel/newAccount.html", context)


@login_required
def deleteAccountView(request, accountName:str, accountId:int):
    account = get_object_or_404(
        ACCOUNTS[accountName], 
        user=request.user, 
        id=accountId
    )

    account.delete()
    
    return redirect(reverse('panel_view'))

@login_required
def deleteTaskView(request, taskId:int):
    task = get_object_or_404(
        Task,
        user=request.user, 
        id=taskId,
    )

    task.delete()
    
    return redirect(reverse('panel_view'))