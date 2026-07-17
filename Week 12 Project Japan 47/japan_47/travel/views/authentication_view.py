from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic import CreateView

from travel.forms import UserForm


class RegisterView(CreateView):
    form_class = UserForm
    template_name = "authentication_pages/register.html"
    success_url = reverse_lazy("travel:home")

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response
