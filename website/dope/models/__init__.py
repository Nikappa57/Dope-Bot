import inspect

from .task import Task
from .paymentMethod import PaymentMethod
from .gateway import Gateway
from .accounts import FootLockerAccount, accountsModule


ACCOUNTS = {
    name: obj for name, obj in inspect.getmembers(accountsModule) 
    if inspect.isclass(obj) and obj.__module__ == accountsModule.__name__
}
