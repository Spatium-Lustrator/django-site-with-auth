from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from . import models
from . import forms

# Create your views here.
def home_view(request):
    return render(request, 'main/home.html')

@login_required
def profile_view(request):
    return render(request, 'main/profile.html')

class RegisterView(FormView):
    form_class = forms.RegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('profile')

    def form_valid(self, form) -> HttpResponse:
        form.save()
        return super().form_valid(form)