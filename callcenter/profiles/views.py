import email
from email import message
from django.shortcuts import redirect, render, get_list_or_404
from django.contrib.auth.decorators import login_required
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
import django.utils
from django.utils.http import urlsafe_base64_decode
from .tokens import account_activation_token

# Create your views here.
@login_required
def show(request):
    template = 'patients/show.html'
    user = request.user
    context = {
        'user': user,
    }
    return render(request, template, context)

def account_activation_sent(request):
    template = 'registration/account_activation_sent.html'
    user = request.user
    context = {
        'user': user,
    }
    return render(request, template, context)

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = '112 Горяцая линия, подтверждение регистрации'
            message = render_to_string('account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('account_activation_sent')
    else:
        form = SignUpForm()
        template = 'registration/signup.html'
        context = {
            'form': form
        }
    return render(request, template, context)

def activate(request, uidb64, token):
    try:
        uid = django.utils.encoding.force_text(urlsafe_base64_decode(uidb64))
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
        return render(request, 'account_activation_invalid.html')