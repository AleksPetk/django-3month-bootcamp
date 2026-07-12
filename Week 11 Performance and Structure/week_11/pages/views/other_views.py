import json

from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import ListView, CreateView

from ..forms import CarForm
from ..models import Big, Car
from ..services import generate_ai_helper_answer

def home(request):
    return render(request, "home.html")

@require_POST
def ai_helper_ask(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({
            "success": False,
            "error": "Invalid JSON."
        }, status=400)

    message = data.get("message", "").strip()

    if not message:
        return JsonResponse({
            "success": False,
            "error": "Message cannot be empty."
        }, status=400)

    answer = generate_ai_helper_answer(message)

    return JsonResponse({
        "success": True,
        "answer": answer
    })

class BigListView(ListView):
    model = Big
    template_name = "big.html"
    context_object_name = "bigs"
    paginate_by = 20
    

    def get_queryset(self):
        return Big.objects.select_related("category").all()

class CarListView(ListView):
    model = Car
    template_name = "cars.html"
    context_object_name = "cars"
    paginate_by = 20

class CarCreateView(LoginRequiredMixin, CreateView):
    model = Car
    form_class = CarForm
    template_name = "page_form.html"
    success_url = reverse_lazy("cars")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Create Car"
        context["button_name"] = "Create"
        context["cancel_url"] = "cars"
        return context
