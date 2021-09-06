
from django import forms
from django.contrib import admin

from .models import ACCOUNTS
from .models.accounts import FootLockerAccount
from .models.gateway import Gateway, Suffix
from .models.paymentMethod import PaymentMethod
from .models.task import Task


class GatewayAdminForm(forms.ModelForm):
    class Meta:
        model = Gateway
        fields = '__all__'
        widgets = {
            'supportedAccount': forms.Select(choices=[(name, name) for name in ACCOUNTS.keys()])
        }

class GatewayAdmin(admin.ModelAdmin):
    form = GatewayAdminForm


class SuffixAdmin(admin.ModelAdmin):
    exclude = ('slug',)

# accounts (Solo come Test)
admin.site.register(FootLockerAccount)
################

admin.site.register(Gateway, GatewayAdmin)
admin.site.register(Suffix, SuffixAdmin)
admin.site.register(PaymentMethod)
admin.site.register(Task)



