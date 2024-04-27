from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView, View
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.shortcuts import redirect
import json
from . import models
from . import forms
User = get_user_model()
# Create your views here.
def finish_basic_vote():
    all_entries = []
    # проходимся по 8 регионам
    for region in range(1, 9):
        entries = models.BasicVote.objects.filter(big_region_id=region).order_by('-count_of_votes')[:3]
        all_entries.extend(entries)
    return all_entries

def home_view(request):
    return render(request, 'main/home.html')

def first_vote_view(request):
    context = {"list_of_good_regions":finish_basic_vote()}
    return render(request, "main/first_vote.html", context)

def basic_vote_view(request):
    # votes_set = models.Vote.objects.all()
    # trails_set = models.Trail.objects.all()
    # vote_ids = [vote.vote_trail_id for vote in sorted(votes_set, key=lambda trail: trail.vote_count_of_votes, reverse=True)]
    # votes = [vote.vote_count_of_votes for vote in sorted(votes_set, key=lambda trail: trail.vote_count_of_votes, reverse=True)]
    # votes_and_indexes = {vote.vote_trail_id:vote.vote_count_of_votes for vote in sorted(votes_set, key=lambda trail: trail.vote_count_of_votes, reverse=True)}
    # print(vote_ids)
    # trail_for_vote = [trail for trail in trails_set if trail.id in vote_ids]
    # n = 2
    # context = {"n_best_trails": trail_for_vote, "n_best_votes": json.dumps(votes)}
    return render(request, 'main/basic_vote.html')

def federal_vote_view(request):
    votes_set = models.FederalVote.objects.all()
    trails_set = models.Trail.objects.all()
    vote_ids = [vote.vote_trail_id for vote in sorted(votes_set, key=lambda trail: trail.vote_count_of_votes, reverse=True)]
    print(vote_ids)
    trail_for_vote = [trail for trail in trails_set if trail.id in vote_ids]
    
    context = {"n_best_trails": trail_for_vote[:2]}
    return render(request, 'main/federal_vote.html', context)

@login_required
def profile_view(request):
    return render(request, 'main/profile.html')

@login_required
def vote_view(request):
    votes_set = models.Vote.objects.all()
    trails_set = models.Trail.objects.all()
    vote_ids = [vote.vote_trail_id for vote in votes_set]
    print([trail.id for trail in trails_set])
    trail_for_vote = [trail for trail in trails_set if trail.id in vote_ids]
    print(trail_for_vote[0])
    context = {"first_trail":trail_for_vote[0],"list_of_trails": trail_for_vote[1:]}
    return render(request, 'main/vote.html', context)

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
            return redirect('email_confirmed')
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
        

        




