from django.contrib.auth import login, authenticate, logout
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.http import HttpResponseRedirect
from django.shortcuts import render
from msal import PublicClientApplication

from user.models import ErrorReport, Present, User


def signup(request):
    if 'lang' in request.GET:
        request.session['lang'] = int(request.GET['lang'])
    else:
        request.session['lang'] = request.session.get('lang', 0)
    failed = False
    err_message = ''
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        full_name = request.POST['name']

        # Check if passwords're valid
        if password1 != password2 or len(password1) < 8:
            failed = True
            err_message += 'Bad password. '
        # Check if email's valid
        try:
            validate_email(email)
        except ValidationError:
            failed = True
            err_message += 'Bad email. '
        # If it's all right create user
        if not failed:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1,
                full_name=full_name,
            )
            user.save()
            login(request, user)
    if request.user.is_authenticated:
        page = HttpResponseRedirect(redirect_to='/user')
    else:
        page = render(request, 'register.html', {
            'failed': failed, 'err_message': err_message})
    return page


def msal_signin(request):
    app = PublicClientApplication("4403a646-2af8-42ba-a2b1-4f5a50a5b376",
                                  authority="https://auth.hse.ru/adfs/oauth2/authorize")


def signin(request):
    if 'lang' in request.GET:
        request.session['lang'] = int(request.GET['lang'])
    else:
        request.session['lang'] = request.session.get('lang', 0)
    failed = False
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
        else:
            failed = True
    if request.user.is_authenticated:
        page = HttpResponseRedirect(redirect_to='/user')
    else:
        page = render(request, 'login.html', {'failed': failed})
    return page


def site_logout(request):
    if 'lang' in request.GET:
        request.session['lang'] = int(request.GET['lang'])
    else:
        request.session['lang'] = request.session.get('lang', 0)
    logout(request)
    return render(request, "logout.html")


def profile(request):
    if 'lang' in request.GET:
        request.session['lang'] = int(request.GET['lang'])
    else:
        request.session['lang'] = request.session.get('lang', 0)
    if request.user.is_authenticated:
        page = render(request, "home.html", {"user": request.user})
    else:
        page = render(request, "home.html", {"user": 0})
    return page


def change_lang(request):
    # rus == 0, eng = 1
    lang = request.session.get('lang', 0)
    request.session['lang'] = 1 - lang
    return HttpResponseRedirect(redirect_to='/quest')


def presents(request):
    if 'lang' in request.GET:
        request.session['lang'] = int(request.GET['lang'])
    else:
        request.session['lang'] = request.session.get('lang', 0)

    res = {
        'presents_list': Present.objects.all(),
        'user': request.user,
    }

    if 'present_name' in request.POST:
        req_presetnts = Present.objects.filter(
            present_name_en=request.POST.get('present_name')
        )
        if len(req_presetnts) == 0:
            raise NotImplementedError
        present_cost = req_presetnts[0].present_cost
        if request.user.pts < present_cost:
            res['not_enough'] = True
            return render(request, 'presents.html', res)

        res['req_sent'] = True
        request.user.pts -= present_cost
        request.user.save()

        send_mail(
            subject='Present get',
            message='Получить подарок ' +
                    request.POST.get('present_name') +
                    ' для пользователя ' +
                    request.user.full_name + ' (юзернейм ' +
                    str(request.user) + ')',
            from_email=None,
            recipient_list=['akivanov@edu.hse.ru'],
            fail_silently=False
        )

    return render(request, 'presents.html', res)


def report(request):
    if 'lang' in request.GET:
        request.session['lang'] = int(request.GET['lang'])
    else:
        request.session['lang'] = request.session.get('lang', 0)

    if not request.user.is_authenticated:
        return render(
            request,
            "report.html",
            {
                "user": request.user,
                "not_authenticated": True,
            }
        )

    if 'report' in request.POST:
        rep = ErrorReport(
            error_report=request.POST.get('report', '-1'),
            user=request.user,
        )
        rep.save()
        sent = True
    else:
        sent = False

    return render(
        request,
        'report.html',
        {
            'sent': sent,
            'user': request.user,
        })
