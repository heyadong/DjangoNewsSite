from django.http import JsonResponse
from django.contrib.auth import login,logout,authenticate
from django.views.decorators.http import require_POST
from django.contrib.auth import get_user_model
from utils import restiful
from django.shortcuts import render
from.forms import LoginForm,RegisterForm


@require_POST
def login_view(request):
    form = LoginForm(request.POST)
    if form.is_valid():
        telephone = form.cleaned_data.get('telephone')
        password = form.cleaned_data.get('password')
        remember = form.cleaned_data.get('remember')
        user = authenticate(request,username=telephone,password=password)
        if user:
            if user.is_active:
                login(request,user)  # 登陆
                if remember:
                    request.session.set_expiry(None) # 设置cookies有效期
                else:
                    request.session.set_expiry(0)  # 0是浏览器会话结束时cookies失效
                return restiful.success(message='success')
            else:
                return restiful.unauth(message="用户账号被移除")
        else:
            return restiful.paramserror(message="输入用户名或密码错误")
    else:
        errors = form.get_errors()
        return restiful.paramserror(message=errors)


@require_POST
def register_view(request):
    user = get_user_model()
    form = RegisterForm(request.POST)
    if form.is_valid():
        data = form.cleaned_data
        telephone = data.get('telephone')
        username = data.get('username')
        password = data.get('password1')
        print(telephone,username,password)
        user.object.create_user(username=username, telephone=telephone, password=password)
        return restiful.success(message='注册成功')
    else:
        errors = form.get_errors()
        return restiful.paramserror(message=errors)

