from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponseRedirect
from django import forms


class UserForm(forms.Form):
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(
            attrs={
                "class": "w-full input input-bordered input-primary",
                "placeholder": "Your username",
            }
        ),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "w-full input input-bordered input-primary",
                "placeholder": "Your password",
            }
        )
    )


def index():
    return redirect("network_monitor:index")


def login_view(request):
    if not request.user.is_authenticated:
        form = UserForm(request.POST)
        username_error = None
        password_error = None

        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("network_monitor:index")
            else:
                if not User.objects.filter(username=username).exists():
                    username_error = "Invalid username"
                else:
                    password_error = "Invalid password"

        return render(
            request,
            "users/login.html",
            {
                "form_user": form,
                "username_error": username_error,
                "password_error": password_error,
            },
        )
    else:
        return HttpResponseRedirect(reverse("network_monitor:index"))


def logout_view(request):
    logout(request)
    return redirect("network_monitor:index")
