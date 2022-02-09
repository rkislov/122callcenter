from django.utils.crypto import get_random_string
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required, permission_required
from .models import Videocall
import datetime
from django.contrib.auth.models import User
from profiles.models import Profile



def index(request):
    template = 'video/index.html'
    context = {
        'name': 'test'
    }
    return render(request, template, context)

def generate_link_patient(request):
    chech_videocalls = Videocall.objects.filter(patient=request.user).filter(request=True).filter(success=False)
    if chech_videocalls:
        template='video/exist.html'
        context = {
            'user' : request.user,
        }
        return render(request, template, context)
    else:
        date = datetime.datetime.now().isoformat()
        url_str=get_random_string(length=10)
        patient=request.user
        videocall = Videocall(
            date=date,
            date_of_call=None,
            url_str=url_str,
            patient=patient,
            doctor=None,
            request=True,
            accepted=False,
            success=False,
            nomer_bolnichnogo=None
        )
        videocall.save()
        return redirect('/profiles/lk')



@login_required
def patient_video(request,url_str):
    user=request.user
    template = 'video/index.html'
    context = {
        'user': user,
        'url_str': url_str
    }
    return render(request, template, context)

@login_required
@permission_required('video.view_videocall')
def doctor_video(request,url_str):
    user=request.user
    vcall = Videocall.objects.get(url_str=url_str)
    profile = Profile.objects.get(user=vcall.patient)
    template = 'video/doctor.html'
    context = {
        'user': user,
        'url_str': url_str,
        'vcall': vcall,
        'profile': profile
    }
    return render(request, template, context)

