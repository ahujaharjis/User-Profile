from django.shortcuts import render
from social_django.models import *
from django.contrib.auth.decorators import login_required
from .models import *
from django.shortcuts import redirect
from django.contrib.auth import authenticate as django_authenticate
from django.contrib.auth import login as django_login
from django.utils.encoding import force_text
from django.contrib.auth import logout as django_logout
from .forms import SignUpForm
from django.contrib.sites.shortcuts import get_current_site

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.http import HttpResponse
from .tokens import account_activation_token
# # Create your views here.
def logout(request):
    django_logout(request)
    return redirect('/login_user')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            message = render_to_string('user_profile/account_activation_email.html', {
                'user': user,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)

            return HttpResponse('check mail')
    else:
        form = SignUpForm()
    return render(request, 'user_profile/signup.html', {'form': form})

@login_required
def client(request):
    return render(request,'user_profile/client.html')

def login_user(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = django_authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                django_login(request,user)
                return redirect('user_profile:client')
            else:
                context['message'] = 'Account disabled'
        else:
            context['message'] = "Invalid"
        return render(request, 'registration/login.html', context)
    elif request.user.is_authenticated:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = django_authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                django_login(request, user)
                return redirect('user_profile:client')
            else:
                context['message'] = 'Account Disabled'
        else:
            context['message'] = 'Invalid Login'
        return render(request,'registration/login.html',context)
    else:
        return render(request,'registration/login.html',{'errormsg':'error'})


def account_activation_sent(request):
    return render(request, 'user_profile/account_activation_sent.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = Customer.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Customer.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.email_confirmed = True
        user.save()
        django_login(request, user,backend = 'django.contrib.auth.backends.ModelBackend')
        return client(request)
    else:
        return HttpResponse('The confirmation link was invalid')

@login_required()
def profile(request):
    context = {}
    if request.method == 'POST':
        user = request.user
        un = user.username
        address = request.POST['Address']
        state = request.POST['State']
        city = request.POST['City']
        country = request.POST['Country']
        phone = request.POST.get('Phone','null')
        pincode = request.POST['Pincode']
        if pincode:
            Customer.objects.filter(id=user.id).update(address=address,state=state,city=city,country=country,phone=phone,pincode=pincode)
        else:
            Customer.objects.filter(id=user.id).update(address=address,state=state,city=city,country=country,phone=phone,pincode=None)
        if UserSocialAuth.objects.filter(user_id=user.id).exists():
            context['message'] = "Profile Updated Successfully"
            return render(request,'user_profile/client.html',context)
        else:
            username = request.POST['UserName']
            email = request.POST['Email']
            if un != username:
                if Customer.objects.filter(username=username).exists():
                    context['message']="Username already exists"
                    return render(request,'user_profile/profile.html',context)
            else:
                Customer.objects.filter(id=user.id).update(username=username,email=email)
                context['message'] = "Profile Updated Succesfully"
                return render(request, 'user_profile/client.html', context)



    return render(request,'user_profile/profile.html')