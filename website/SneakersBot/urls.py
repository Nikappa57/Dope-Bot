from django.contrib import admin
from django.urls import path
from django.urls.conf import include

import accounts.views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('panel/', include('dope.urls')),
    path('profile/', accounts.views.profile_view, name='profile_view'),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('paymenys/', include('payments.urls')),
]
