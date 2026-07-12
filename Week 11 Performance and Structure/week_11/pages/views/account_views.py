from django.shortcuts import redirect
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import CreateView

from ..forms import UserForm


class Register(CreateView):
    model = User
    form_class = UserForm
    template_name = "page_form.html"

    success_url = reverse_lazy("home")

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect("home")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        new_user = form.save(commit=False)
        password = form.cleaned_data.get("password")
        new_user.set_password(password)
        new_user.save()
        login(self.request, new_user)
        return redirect("home")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Register"
        context["button_name"] = "Register"
        context["cancel_url"] = "home"
        context["login_url"] = "login"
        return context
