from django.urls.base import reverse
from django.contrib. auth.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from .forms import FormRegistration


@login_required
def profile_view(request):
    context = {'user': request.user}
    return render(request, 'accounts/profile.html', context)


def register_view(request):
    if request.user.is_authenticated:
        return redirect('panel_view')
        
    if request.method == "POST":
        form = FormRegistration(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["username"]

            User.objects.create_user(
                username=username,
                password=password,
                email=email,
            )

            user = authenticate(username=username, password=password)
            login(request, user)

            return redirect(reverse('panel_view'))
    else:
        form = FormRegistration()

    context = {'form': form}

    return render(request, "registration/registration.html", context)