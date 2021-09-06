from .views.localApi import getPriceOfPlanApi
from django.urls import path
from .views.planCreateEdit import chooseDetailsPlan, chooseGatewayPlan, modifyDetailsPlan, renewPlan

urlpatterns = [
    path('chose-your-plan/', chooseGatewayPlan, name='choose_gateway_plan'),
    path('chose-your-plan/<str:gateways>/', chooseDetailsPlan, name='choose_details_plan'),
    path('modify-your-plan/<int:permissionId>/', modifyDetailsPlan, name='modify_details_plan'),
    path('renew-your-plan/<int:permissionId>/', renewPlan, name='renew_plan'),

    path('api/local/get-price-of-plan/<str:gateway>/<int:tasks>/<int:month>/', getPriceOfPlanApi, name='get_price_of_plan')
]
