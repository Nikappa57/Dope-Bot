
import pytz

from typing import Any, Dict, List, Tuple

from django.contrib.auth.models import User

from dope.models.task import Task
from dope.models.item import Item
from dope.models.gateway import Suffix
from dope.utils.productModel import Product
from .footlocker import getDropListFootLocker, getProductFootLocker
from .productModel import Product

def createNewTask(gateway: Suffix, user: User, product: Product, productInfo: Dict[str, Tuple[str, str]], account: Any) -> None:
    # TODO: COUPONS
    item = Item.objects.filter(sku=product.sku)
    
    if not item.exists():
        item = Item.createFromProduct(product=product, data=productInfo)
    else:
        item = item.first()
    
    new_task = Task(
        user=user,
        gateway=gateway,
        item=item,
        date=product.relaseDate,
    )

    if gateway.gateway.name == gateway.gateway.FOOTLOCKER:
        new_task.footLockerAccount = account

    new_task.save()

def getDropList(gateway: Suffix) -> List:
    if gateway.gateway.name == gateway.gateway.FOOTLOCKER:
        return getDropListFootLocker(gateway)

def getProduct(gateway: Suffix, sku: str) -> Dict[str, Any]:
    if gateway.gateway.name == gateway.gateway.FOOTLOCKER:
        return getProductFootLocker(gateway, sku)


