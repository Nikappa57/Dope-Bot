
from django.urls import reverse
from django.http import Http404
from django.core.paginator import Paginator
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required

from core.decorators.permission import add_task_required

from dope.models import ACCOUNTS
from dope.models.gateway import Gateway, Suffix
from dope.forms import genDetailsForm
from dope.utils import createNewTask, getDropList, getProduct


@login_required
def selectGatewayView(request):
    context = {'gateways': Gateway.getAllUrls()}

    return render(request, "dope/newTask/select-gateway.html", context)


@login_required
@add_task_required
def selectItemView(request, gatewaySuffix:Suffix, gateway:Gateway):
    product_list = getDropList(gatewaySuffix)
    
    if not product_list:
        return render(request, "dope/newTask/no-item.html")

    paginator = Paginator(product_list, per_page=12)
    page = request.GET.get('page')
    
    if not page:
        page = 1
    
    products = paginator.get_page(page)

    context = {'products': products, 'gatewaySlug': gatewaySuffix.slug, "page": paginator.page(page)}
    return render(request, "dope/newTask/select-item.html", context)


@login_required
@add_task_required
def selectDetailsView(request, gatewaySuffix:Suffix, gateway:Gateway, sku):
    accounts = ACCOUNTS[gateway.supportedAccount].objects.filter(
        gateway=gateway, user=request.user)
    
    if not accounts.exists():
        return redirect("{}?next={}".format(
            reverse('add_account_view', args=[gateway.name]), 
            reverse('select_details_view', args=[gatewaySuffix.slug, sku]),
        ))

    product = getProduct(gatewaySuffix, sku)

    if request.method == "POST":
        form = genDetailsForm(
            choices=product["choices"], 
            user=request.user, 
            request=request.POST, 
            gateway=gateway
        )

        if form.is_valid():
            account_model = ACCOUNTS[gateway.supportedAccount]
            account_id = form.cleaned_data["accountId"]
            account = get_object_or_404(account_model, id=account_id)
            
            if account.user != request.user:
                raise Http404('Account error')
        
            createNewTask(
                gateway=gatewaySuffix,
                user=request.user,
                product=product["obj"],
                productInfo=product["choices"],
                account=account,
            )

            return redirect(reverse('panel_view'))
    else:
        form = genDetailsForm(
            choices=product["choices"], 
            user=request.user, 
            gateway=gateway
        )

    context = {'form': form, 'product': product['obj']}
    return render(request, "dope/newTask/select-details.html", context)