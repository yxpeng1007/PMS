from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth import (
    authenticate,
    login as django_login,
    get_user_model,
)
from django.views.decorators.http import require_http_methods
from app01.forms.userForm import CustomUserCreationForm
from app01.forms.passwordResetForm import PasswordResetForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from app01.forms.CourseForm import CourseForm
from app01.models import Course
from datetime import datetime, timedelta, timezone
from django.contrib import messages

User = get_user_model()


def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                django_login(request, user)
                return redirect("home")  # 假设登录后重定向到首页
            else:
                context = {"form": form, "error": "账号或密码不正确"}
                return render(request, "login.html", context)
        else:
            context = {"form": form, "error": "表单验证失败"}
            return render(request, "login.html", context)
    else:
        form = AuthenticationForm()
        return render(request, "login.html", {"form": form})


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            django_login(request, user)
            return redirect("home")
        else:
            context = {"form": form, "error": "Invalid registration data"}
            return render(request, "register.html", context)
    else:
        form = CustomUserCreationForm()
        return render(request, "register.html", {"form": form})


# 忘记密码页面的视图函数（需要实现）
def forgot_password(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            phone_number = form.cleaned_data["phone_number"]
            users = get_user_model().objects.filter(
                username=username, phone_number=phone_number
            )

            if users.exists():
                # 将密码重置为用户输入的密码
                user = users.first()
                user.set_password(form.cleaned_data["password"])
                user.save()
                return redirect("login")  # 重定向到登录页面
            else:
                context = {"form": form, "error": "用户不存在"}
                return render(request, "forgot_password.html", context)
    else:
        form = PasswordResetForm()
        return render(request, "forgot_password.html", {"form": form})


# 忘记密码页面的视图函数（需要实现）
def forgot_password_phone(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            phone_number = form.cleaned_data["phone_number"]
            users = get_user_model().objects.filter(
                username=username, phone_number=phone_number
            )

            if users.exists():
                # 将密码重置为用户输入的密码
                user = users.first()
                user.set_password(form.cleaned_data["password"])
                user.save()
                return redirect("login")  # 重定向到登录页面
            else:
                context = {"form": form, "error": "用户不存在"}
                return render(request, "forgot_password_phone.html", context)
    else:
        form = PasswordResetForm()
        return render(request, "forgot_password_phone.html", {"form": form})


@csrf_exempt  # 允许跨站请求，注意：生产环境中应谨慎使用
@require_http_methods(["POST"])
def forgot_password_check(request):
    username = request.POST.get("username")
    email = request.POST.get("email")
    user = User.objects.filter(username=username, email=email).first()

    if user:
        request.session["reset_username"] = user.username
        return JsonResponse({"success": True})
    else:
        return JsonResponse({"success": False})


@csrf_exempt  # 允许跨站请求，注意：生产环境中应谨慎使用
@require_http_methods(["POST"])
def forgot_password_phone_check(request):
    username = request.POST.get("username")
    phone_number = request.POST.get("phone_number")
    user = User.objects.filter(
        username=username, phone_number=phone_number
    ).first()

    if user:
        request.session["reset_username"] = user.username
        return JsonResponse({"success": True})
    else:
        return JsonResponse({"success": False})


def reset_password(request):
    if request.method == "POST":
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        username = request.session.get("reset_username")

        if password != confirm_password:
            return render(
                request,
                "reset_password.html",
                {"error": "Passwords do not match"},
            )

        if username:
            user = User.objects.get(username=username)
            user.set_password(password)
            user.save()
            return redirect("login")
        else:
            return render(
                request, "reset_password.html", {"error": "Invalid request"}
            )
    else:
        return render(request, "reset_password.html")


# 登录页面的视图函数
def home(request):
    # 只有登录后才能访问的首页
    return render(request, "home.html")


def index(request):
    return render(request, "index.html")


@login_required
def add_course(request):
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            # 获取数据
            day_of_week = form.cleaned_data["day_of_week"]
            time_slot = form.cleaned_data["time_slot"]
            user = request.user

            # 检查冲突
            if Course.objects.filter(
                user=user, day_of_week=day_of_week, time_slot=time_slot
            ).exists():

                return JsonResponse(
                    {"status": "error", "message": "该时间段的课程已存在"}
                )

            # 保存课程
            course = form.save(commit=False)  # 创建课程实例但不立即保存到数据库
            course.user = request.user  # 将当前用户设置为课程的用户
            course.save()  # 保存到数据库
            return JsonResponse({"status": "success"})
        else:

            return JsonResponse({"status": "error", "errors": form.errors})
    else:
        form = CourseForm()

    return render(request, "add_course.html", {"form": form})


@login_required
def home(request):
    user = request.user
    courses = request.user.courses.all()  # 获取当前用户的课程
    form = CourseForm()  # 创建一个空的表单
    print(courses)

    # 获取 session 中的 start_date，如果不存在则初始化为今天的日期
    start_date_str = request.session.get("start_date")
    if not start_date_str:
        # 如果 session 中没有 start_date，初始化为本周的周一
        today = datetime.today()
        start_date = today - timedelta(days=today.weekday())  # 获取本周的周一
        request.session["start_date"] = start_date.strftime(
            "%Y-%m-%d"
        )  # 存储到 session
    else:
        # 如果 session 中有 start_date，将其转换为 datetime 对象
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")

    # 生成日期列表，从周一开始到周日
    dates = [
        (start_date + timedelta(days=i)).strftime("%m-%d") for i in range(7)
    ]
    days = [
        "周一",
        "周二",
        "周三",
        "周四",
        "周五",
        "周六",
        "周日",
    ]  # 定义星期几

    context = {
        "username": user.username,
        "email": user.email,
        "phone_number": user.phone_number,
        "signature": user.signature,  # 个性签名
        "avatar": (
            user.avatar.url if user.avatar else "default-avatar.png"
        ),  # 头像
    }

    return render(
        request,
        "home.html",
        {"courses": courses, "form": form, "dates": dates, "days": days},
    )


@login_required
def delete_course(request):
    if request.method == "POST":
        course_id = request.POST.get("course_id")  # 获取选择的课程ID
        try:
            # 查找当前用户的课程，确保只有该用户的课程可以被删除
            course = Course.objects.get(id=course_id, user=request.user)
            course.delete()  # 删除课程
            return JsonResponse({"status": "success"})  # 返回成功状态
        except Course.DoesNotExist:
            return JsonResponse(
                {"status": "error", "message": "课程不存在"}
            )  # 返回错误状态
    return JsonResponse(
        {"status": "error", "message": "请求方式错误"}
    )  # 请求方式不正确时的错误响应


@login_required
def change_week(request):
    if request.method == "GET":
        # 获取当前存储在 session 中的开始日期
        start_date_str = request.session.get("start_date", None)
        if start_date_str:
            # 将字符串转换为日期对象
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        else:
            # 默认使用当前日期的本周一
            today = timezone.now()
            start_date = today - timedelta(days=today.weekday())

        # 获取请求中的偏移量并计算新的开始日期
        offset = int(request.GET.get("offset", 0))
        new_start_date = start_date + timedelta(weeks=offset)

        # 更新 session 中的开始日期
        request.session["start_date"] = new_start_date.strftime("%Y-%m-%d")

        return JsonResponse({"success": True})

    return JsonResponse({"success": False}, status=400)


@login_required
def information(request):
    user = request.user

    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        phone_number = request.POST.get("phone")
        current_password = request.POST.get("current_password")
        new_password = request.POST.get("new_password")
        signature = request.POST.get("signature")
        # 处理用户信息更新
        user.username = username
        user.email = email
        user.phone_number = phone_number  # 确保该属性存在于用户模型中
        user.signature = signature  # 更新个性签名

        # 处理头像更新
        if request.FILES.get("avatar"):
            user.avatar = request.FILES["avatar"]  # 更新头像
        # 处理密码更新
        if current_password and new_password:
            # 检查原密码是否正确
            if not user.check_password(current_password):
                return JsonResponse(
                    {"error": "原密码错误，请重新输入"}, status=400
                )

            # 检查新密码是否符合要求
            if len(new_password) < 6 or len(new_password) > 10:
                return JsonResponse(
                    {"error": "新密码长度要求为6-10位"}, status=400
                )

            # 更新密码
            user.set_password(new_password)
            update_session_auth_hash(request, user)  # 保持用户登录状态

        user.save()  # 保存用户信息
        messages.success(request, "信息修改成功")
        return JsonResponse({"success": "信息修改成功"})

    context = {
        "username": user.username,
        "email": user.email,
        "phone_number": user.phone_number,
        "signature": user.signature,  # 个性签名
        "avatar": (
            user.avatar.url if user.avatar else "default-avatar.png"
        ),  # 头像
    }

    return render(request, "information.html", context)
