from typing import Any
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import DeleteView
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages

from cart.models import Cart

from .forms import NewUserForm

# Create your views here.
def signup(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, "Registration successful." )
            return redirect("home")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request=request, template_name="account/signup.html", context={"register_form":form, 'messages':get_messages(request)})

@login_required(login_url="/account/login/")
def index(request):
    return render(request, 'account/index.html',  {'messages':get_messages(request), 'cart_length': Cart.get_cart_length(request.user)})

@login_required(login_url="/account/login/")
def profile(request):
    return render(request, 'account/profile.html', {'messages':get_messages(request), 'cart_length': Cart.get_cart_length(request.user)})

@login_required(login_url="/account/login/")
def logout_view(request):
    logout(request)
    return redirect('home')

class UserDelete(DeleteView):
    model = get_user_model()
    success_url = reverse_lazy('home')
    template_name = 'account/delete.html'

    def get_queryset(self):
        pk = self.kwargs.get(self.pk_url_kwarg)
        if self.request.user.id == pk:
            return super().get_queryset()
        return super().get_queryset().none()
