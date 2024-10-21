from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login as django_login, get_user_model
from django.views.decorators.http import require_http_methods
from app01.forms.userForm import CustomUserCreationForm
from app01.forms.passwordResetForm import PasswordResetForm
from django.contrib.auth.forms import AuthenticationForm

User = get_user_model()

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

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            django_login(request, user)
            return redirect('home')
        else:
            context = {'form': form, 'error': 'Invalid registration data'}
            return render(request, 'register.html', context)
    else:
        form = CustomUserCreationForm()
        return render(request, 'register.html', {'form': form})

# 忘记密码页面的视图函数（需要实现）
def forgot_password(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            phone_number = form.cleaned_data['phone_number']
            users = get_user_model().objects.filter(username=username, phone_number=phone_number)
            
            if users.exists():
                # 将密码重置为用户输入的密码
                user = users.first()
                user.set_password(form.cleaned_data['password'])
                user.save()
                return redirect('login')  # 重定向到登录页面
            else:
                context = {'form': form, 'error': '用户不存在'}
                return render(request, 'forgot_password.html', context)
    else:
        form = PasswordResetForm()
        return render(request, 'forgot_password.html', {'form': form})
    
@require_http_methods(["POST"])
def forgot_password_check(request):
    username = request.POST.get('username')
    email = request.POST.get('email')
    user = User.objects.filter(username=username, email=email).first()
    
    if user:
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})

def reset_password(request):
    return render(request, 'reset_password.html')

# 登录页面的视图函数
def home(request):
    # 只有登录后才能访问的首页
    return render(request, 'home.html')

def index(request):
    return render(request, 'index.html')