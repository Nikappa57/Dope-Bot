from typing import Dict, Tuple
from django import forms
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from dope.models import ACCOUNTS
from dope.models.gateway import Gateway


def genDetailsForm(choices:Dict[str, Tuple[Tuple[str]]], user:User, gateway:Gateway, request=None):
    accounts = ACCOUNTS[gateway.supportedAccount].objects.filter(gateway=gateway, user=user)
    
    # TODO: add other info for name
    ACC_CHOICES = [(account.id, account.name) for account in accounts]

    class DetailsForm(forms.Form):
        def __init__(self, *args, **kwargs) -> None:
            super(DetailsForm, self).__init__(*args, **kwargs)

            for name, options in choices.items():
                self.fields[name] = forms.ChoiceField(choices=options)

        accountId = forms.ChoiceField(choices=ACC_CHOICES)
    
    return DetailsForm(request)

def genAccountForm(modelName:str, request=None, *args, **kwargs):
    assert modelName in ACCOUNTS.keys()

    class AccountForm(forms.ModelForm):
        
        class Meta:
            model = ACCOUNTS[modelName]
            fields = "__all__"
            exclude = ("user", "gateway",)

    return AccountForm(request, *args, **kwargs)

