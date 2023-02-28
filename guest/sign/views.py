from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from sign.models import Event, Guest


# Create your views here.
def index(request):
    return render(request, "index.html")


# 登录动作
def login_action(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        # if username == 'admin' and password == 'admin123':
        #     response = HttpResponseRedirect('/event_manage/')
        #     # response.set_cookie('user', username, 3600)
        #     request.session['user'] = username
        #     return response
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            request.session['user'] = username
            response = HttpResponseRedirect('/event_manage/')
            return response

        else:
            return render(request, 'index.html', {'error': 'username or password error!'})


# 发布会管理
@login_required
def event_manage(request):
    # username = request.COOKIES.get('user', '')
    event_list = Event.objects.all()
    username = request.session.get('user', '')
    return render(request, 'event_manage.html', {"user": username, "events": event_list})


# 活动页关键字搜索
@login_required
def search_name(request):
    username = request.session.get('user', '')
    search_name = request.GET.get("name", '')
    event_list = Event.objects.filter(name__contains=search_name)
    return render(request, "event_manage.html", {"user": username, "events": event_list})


# 嘉宾管理
@login_required
def guest_manage(request):
    # username = request.COOKIES.get('user', '')
    username = request.session.get('user', '')
    guest_list = Guest.objects.all()
    paginator = Paginator(guest_list, 2)
    page = request.GET.get('page')
    try:
        contracts = paginator.page(page)
    except PageNotAnInteger:
        contracts = paginator.page(1)
    except EmptyPage:
        contracts = paginator.page(paginator.num_pages)
    return render(request, 'guest_manage.html', {"user": username, "guests": contracts})


# 嘉宾页关键字搜索
@login_required
def search_guest_name(request):
    username = request.session.get('user', '')
    guest_name = request.GET.get("realname", '')
    guest_list = Guest.objects.filter(realname__contains=guest_name)
    paginator = Paginator(guest_list, 2)
    page = request.GET.get('page')
    try:
        contracts = paginator.page(page)
    except PageNotAnInteger:
        contracts = paginator.page(1)
    except EmptyPage:
        contracts = paginator.page(paginator.num_pages)
    return render(request, "guest_manage.html", {"user": username, "guests": contracts})


# 签到功能
@login_required
def sign_index(request, eid):
    event = get_object_or_404(Event, id=eid)
    guest_list = Guest.objects.filter(event_id=eid)
    sign_list = Guest.objects.filter(event_id=eid, sign='1')
    guest_data = str(len(guest_list))
    sign_data = str(len(sign_list))
    return render(request, 'sign_index.html', {'event': event, 'guest_num': guest_data, 'sign_num': sign_data})


# 签到动作
@login_required
def sign_index_action(request, eid):
    event = get_object_or_404(Event, id=eid)
    guest_list = Guest.objects.filter(event_id=eid)
    sign_list = Guest.objects.filter(event_id=eid, sign='1')
    guest_data = str(len(guest_list))
    sign_data = str(len(sign_list))
    phone = request.POST.get('phone')
    print(phone)
    result = Guest.objects.filter(phone=phone)
    if not result:
        return render(request, 'sign_index.html', {"event": event, "hint": 'phone error!', 'guest_num': guest_data,
                                                   'sign_num': sign_data})
    result = Guest.objects.filter(phone=phone, event_id=eid)
    if not result:
        return render(request, 'sign_index.html', {"event": event, "hint": 'event id or phone error.',
                                                   'guest_num': guest_data, 'sign_num': sign_data})
    result = Guest.objects.get(phone=phone, event_id=eid)
    if result.sign:
        return render(request, 'sign_index.html', {'event': event, 'hint': 'user has sign in.',
                                                   'guest_num': guest_data, 'sign_num': sign_data})
    else:
        Guest.objects.filter(phone=phone, event_id=eid).update(sign='1')
        sign_list = Guest.objects.filter(event_id=eid, sign='1')
        sign_data = str(len(sign_list))
        return render(request, 'sign_index.html', {"event": event, 'hint': 'sign in success.', 'guest': result,
                                                   'guest_num': guest_data, 'sign_num': sign_data})
