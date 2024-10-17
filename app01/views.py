from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as django_login
from app01.forms.userForm import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                django_login(request, user)
                return redirect('home')  # 假设登录后重定向到首页
            else:
                context = {'form': form, 'error': '账号或密码不正确'}
                return render(request, 'login.html', context)
        else:
            context = {'form': form, 'error': '表单验证失败'}
            return render(request, 'login.html', context)
    else:
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})

# 注册页面的视图函数（需要实现）
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # 重定向到登录页面
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

# 忘记密码页面的视图函数（需要实现）
def forgot_password(request):
    # 实现忘记密码逻辑
    pass

# 登录页面的视图函数
def home(request):
    # 只有登录后才能访问的首页
    return render(request, 'home.html')

def index(request):
    return render(request, 'index.html')