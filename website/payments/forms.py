from typing import List
from django import forms
from django.db.models import Q

from dope.models.gateway import Gateway


def genGatewayPlanForm(request=None, excludedGateways:List[Gateway]=[], *args, **kwargs):
    gateways = Gateway.objects.filter(~Q(id__in=[g.id for g in excludedGateways]))
    CHOICES = ((g.name, g.name) for g in gateways)
    
    class GatewayPlanForm(forms.Form):
        gateways = forms.MultipleChoiceField(choices=CHOICES, widget=forms.CheckboxSelectMultiple)

    return GatewayPlanForm(request, *args, **kwargs)


def genDetailsPlanForm(gateways:List[str], request=None, timeField:bool=True, initalTasks:int=None, minTasksValue:int=0, *args, **kwargs):
    
    class DetailsPlanForm(forms.Form):
        def __init__(self, *args, **kwargs) -> None:
            super(DetailsPlanForm, self).__init__(*args, **kwargs)

            for name in gateways:
                gateway:Gateway = Gateway.objects.filter(name=name).first()
                if timeField:
                    TIME_CHOICES = ((p.month, "{} month".format(p.month)) for p in gateway.pricing.all())
                    self.fields["{}-time".format(name)] = forms.ChoiceField(choices=TIME_CHOICES, label="{} Time".format(name)) # attrs={'type': 'range'}

                TASK_CHOICES = ((n, n) for n in range(1, gateway.maxTaskForAccount + 1) if n > minTasksValue)
                self.fields["{}-tasks".format(name)] = forms.ChoiceField(choices=TASK_CHOICES, label="{} Task".format(name))

                if initalTasks:
                    self.fields["{}-tasks".format(name)].initial = initalTasks
    return DetailsPlanForm(request, *args, **kwargs)
