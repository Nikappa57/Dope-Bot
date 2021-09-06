from django.urls import path
from django.urls.conf import include

from dope.views import newTask, panel

urlpatterns = [
    path('', panel.panelView, name='panel_view'),
    path('add-account/<str:gateway>', panel.addAccountView, name='add_account_view'),
    path('edit-account/<str:gateway>/<int:accountId>',  panel.editAccountView, name='edit_account_view'),
    path('delete-account/<str:accountName>/<int:accountId>',  panel.deleteAccountView, name='delete_account_view'),
    path('delete-task/<int:taskId>',  panel.deleteTaskView, name='delete_task_view'),
    path('new-task/',  newTask.selectGatewayView, name='select_gateway_view'),
    path('new-task/<str:gatewaySlug>',  newTask.selectItemView, name='select_item_view'),
    path('new-task/<str:gatewaySlug>/<str:sku>/',  newTask.selectDetailsView, name='select_details_view'),
]
