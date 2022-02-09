from ast import If
import email
from email import message
import re
from django.shortcuts import redirect, render, get_list_or_404
from django.contrib.auth.decorators import login_required
from .models import Profile
from calls.models import Journal, Subject, Sub_subject, Patient, Manipulation, City, Hospital, Call_result, Address, Call 
import datetime
from django.contrib.auth.models import User
from django.contrib.auth.decorators import permission_required
from callcenter.settings import EMAIL_HOST_USER
from django.core.mail import utils,EmailMessage
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from .forms import SignUpForm
from .tokens import account_activation_token
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.utils import encoding
from django.utils.http import urlsafe_base64_decode
from .tokens import account_activation_token
from video.models import Videocall
from django.contrib.auth import authenticate

# Create your views here.
@login_required
def show(request):
    if request.user.has_perm('video.view_videocall'):
        return redirect('doctors:lk')
    else: 
        template = 'patients/show.html'
        user = request.user
        vcalls = Videocall.objects.filter(patient=user)[:10]
        if Profile.objects.get(user=user).exists():
            profile = Profile.objects.get(user=user)
        else:
            profile = None
        if vcalls:
            vcalls = vcalls
        else:
            vcalls = None
        context = {
            'user': user,
            'vcalls': vcalls,
            'profile': profile
        }
        return render(request, template, context)

@login_required
def edit(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.save()
        profileid=request.POST.get('profileid')
        snils = request.POST.get('snils').strip()
        medpolis = request.POST.get('medpolis').strip()
        mobile = request.POST.get('mobile').strip()
        if profileid:
            profile = Profile.objects.get(id=profileid)
            profile.snils = snils
            profile.medpolis = medpolis
            profile.mobile = mobile
            profile.save()
            return redirect('/profiles/lk')
        else:
            profile = Profile(
                user=user,
                snils=snils,
                medpolis=medpolis,
                mobile=mobile,
            )
            profile.save()
            return redirect('/profiles/lk')
            
    else:
        template = 'patients/edit.html'
        user = request.user
        profile = Profile.objects.get(user=user)
        context = {
            'user': user,
            'profile': profile
        }
        return render(request, template, context)

def account_activation_sent(request):
    template = 'registration/account_activation_sent.html'
    user = request.user
    profile = Profile.objects.filter(user=user)
    context = {
        'user': user,
        'profile': profile
    }
    return render(request, template, context)


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  
            # load the profile instance created by the signal
            user.save()
            raw_password = form.cleaned_data.get('password1')
 
            # login user after signing up
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
 
            # redirect user to home page
            return redirect('/profiles/lk')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})
# def signup(request):
#     if request.method == 'POST':
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.is_active = False
#             user.save()
#             current_site = get_current_site(request)
#             subject = '112 Горяцая линия, подтверждение регистрации'
#             message = render_to_string('registration/account_activation_email.html', {
#                 'user': user,
#                 'domain': current_site.domain,
#                 'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#                 'token': account_activation_token.make_token(user),
#             })
#             user.email_user(subject, message)
#             return redirect('profiles:account_activation_sent')
#     else:
#         form = SignUpForm()
#     return render(request, 'registration/signup.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = encoding.force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'registration/account_activation_invalid.html')