import requests
import random
import hashlib
import base64

from django.contrib.auth import logout, get_user_model, login
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy, reverse
from . import models
from . import forms
from .models import Trail, CurrentState, BasicVote

User = get_user_model()


def createPay(amount):
    public_key = "yzr64tnue9w75g1"
    shop_id = "6113"

    try:
        random_number = random.randint(0, 999999999)  # Генерируем случайное число от 0 до 999999999
        hash_str = f'{shop_id}{amount}{public_key}{random_number}'

        hash = hashlib.sha256(hash_str.encode('utf-8')).hexdigest()

        create_pay = requests.get(
            f'https://sci.fropay.bar/get?amount={amount}&desc=MTAyMTU=&shop_id={shop_id}&label={random_number}&hash={hash}&nored=1')

        payments_id = create_pay.json()['id']
        pay_url = create_pay.json()['url']

        return {'bill': payments_id, 'url': pay_url}
    except:
        return 'False'


def home_view(request):
    return render(request, 'main/Home.html', {"home": True})


def validate_trops_view(request):
    all_trops = Trail.objects.all()
    return render(request, 'main/trops.html', {"trops": all_trops})


def some_trop_view(request, route_id):
    print(route_id)
    return render(request, 'main/trops.html')


@login_required
def go_some_trop_view(request, route_id):
    user = request.user
    user.current_trail = Trail.objects.get(id=route_id)
    user.save()
    visited_trails = user.get_visited_trails()
    current_trail = user.get_current_trail()
    return render(request, 'main/history.html', {"trops": visited_trails, "current_trail": current_trail})


@login_required
def end_some_trop_view(request, route_id):
    user = request.user
    user.end_hike()
    visited_trails = user.get_visited_trails()
    current_trail = user.get_current_trail()
    return render(request, 'main/history.html', {"trops": visited_trails, "current_trail": current_trail})


@login_required
def profile_view(request):
    return render(request, 'main/profile.html')


@csrf_exempt
@login_required
def change_state(request):
    state = CurrentState.objects.get(id=1)
    if request.method == 'GET':
        if state.basic_state:
            return render(request, 'main/change_state.html', {"basic": True})
        elif state.federal_state:
            return render(request, 'main/change_state.html', {"federal": True})
        else:
            top_ten = 10
            return render(request, 'main/change_state.html', {"federal": True})
    elif request.method == 'POST':
        if state.basic_state:
            state.basic_state = 0
            state.federal_state = 1
            state.save()
            return render(request, 'main/change_state.html', {"federal": True})
        elif state.federal_state:
            state.federal_state = 0
            state.basic_state = 0
            state.save()
            return render(request, 'main/change_state.html', {"basic": True})


@login_required
def history_view(request):
    user = request.user
    visited_trails = user.get_visited_trails()
    current_trail = user.get_current_trail()
    return render(request, 'main/history.html', {"trops": visited_trails, "current_trail": current_trail})


@login_required
def vote_some_trop_view(request, route_id):
    trail = Trail.objects.get(id=route_id)
    if trail.trail_is_on_vote:
        user = request.user
        user.number_of_votes = user.number_of_votes - 1
        user.save()
        trail.trail_votes.add(user)
        trail.save()
        return render(request, 'main/VoteForTrail.html', {"trail": trail})
    else:
        return render(request, 'main/home.html')


@login_required
def donate_some_trop_view(request, route_id):
    trail = Trail.objects.get(id=route_id)
    user = request.user
    user.user_balance = user.user_balance - 250
    user.save()
    return render(request, 'main/VoteForTrail.html', {"trail": trail})


@login_required
def select_some_trop_view(request, route_id):
    trail = Trail.objects.get(id=route_id)
    return render(request, 'main/VoteForTrail.html', {"trail": trail})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))


@csrf_exempt
@login_required
def add_money_view(request, sum):
    user = request.user
    user.number_of_votes = user.number_of_votes + 100
    user.save()
    url = createPay(amount=sum)
    print(url)
    return JsonResponse({"url": url})


class RegisterView(FormView):
    form_class = forms.RegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('profile')

    def form_valid(self, form) -> HttpResponse:
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        activation_url = reverse_lazy('confirm_email', kwargs={'uidb64': uid, 'token': token})
        send_mail(
            'Подтвердите свой электронный адрес',
            f'Пожалуйста, перейдите по следующей ссылке, чтобы подтвердить свой адрес электронной почты: http://127.0.0.1:8000{activation_url}',
            'service.notehunter@gmail.com',
            [user.email],
            fail_silently=False,
        )
        return redirect('email_confirmation_sent')


class EmailConfirmationSentView(TemplateView):
    template_name = 'registration/email_confirmation_sent.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Письмо активации отправлено'
        return context


class UserConfirmEmailView(View):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('profile')
        else:
            return redirect('email_confirmation_failed')


class EmailConfirmedView(TemplateView):
    template_name = 'registration/email_confirmed.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ваш электронный адрес активирован'
        return context


class EmailConfirmationFailedView(TemplateView):
    template_name = 'registration/email_confirmation_failed.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ваш электронный адрес не активирован'
        return context
