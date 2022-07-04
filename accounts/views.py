from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
#from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm, CustomPasswordChangeForm

# SMTP
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.core.mail import EmailMessage, send_mail
from django.template.loader import render_to_string

from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token


def signup(request):
    if request.method == 'POST':
        signup_form = SignUpForm(request.POST)

        print(signup_form)

        if signup_form.is_valid():
            user_instance = signup_form.save(commit=False)
            user_instance.is_active = False
            user_instance.set_password(signup_form.cleaned_data['password1'])
            print("user_instance : ", user_instance)
            print("email : ", user_instance.email)
            user_instance.save()

            current_site = get_current_site(request)
            msg_html = render_to_string('accounts/VerifyEmail.html',
                                        {'user': user_instance,
                                         'domain': current_site.domain,
                                         'uid': urlsafe_base64_encode(force_bytes(user_instance.pk)),
                                         'token': account_activation_token.make_token(user_instance)})
            msg = EmailMessage(subject="[단축 URL 서비스] 회원가입 인증 메일", body=msg_html,
                               from_email="s340f914ss@gmail.com", to=[user_instance.email])
            msg.content_subtype = 'html'
            msg.send()

            return render(request, "accounts/email_send.html")
    else:
        signup_form = SignUpForm()
        print("잘못된 회원 가입 정보 입력")

    return render(request, 'accounts/signup.html', {'form': signup_form})


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(id=uid)
    except(TypeError, ValueError):
        user = None

    if user and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.info(request, '계정이 활성화 되었으니 로그인하세요!')
        return render(request, "accounts/email_success.html")
    else:
        messages.error(request, "이미 사용한 토큰입니다.")
        return render(request, "accounts/email_fail.html")


@login_required
def password_change(request):
    if request.method == 'POST':
        password_change_form = CustomPasswordChangeForm(
            request.user, request.POST)
        if password_change_form.is_valid():
            user = password_change_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "비밀번호를 성공적으로 변경하였습니다.")
            return redirect('/')
    else:
        password_change_form = CustomPasswordChangeForm(request.user)

    return render(request, 'accounts/change_password.html', {'password_change_form': password_change_form})


@login_required
def user_withdrawal(request):
    if request.method == 'POST':
        try:
            #user = User.objects.get(username=request.user)
            user = User.objects.filter(username__exact=request.user)
            active = user.values('is_active').get()

            if active['is_active']:
                user.update(is_active=False)

            return redirect('/')

        except(ValueError):
            print("사용자를 찾을 수 없습니다.")

    return render(request, 'accounts/user_withdrawal.html')

# 아이디 찾기


def find_id(request):
    if request.method == 'POST':
        try:
            email = request.POST.get('email')
            user = User.objects.filter(email__exact=email)
            username = user.values('username').get()
            register_email = user.values('email').get()

            find_id = username['username']
            reg_email = register_email['email']

            # email로 아이디 전송
            current_site = get_current_site(request)

            msg_html = render_to_string(
                'accounts/FindID_Email.html', {'user': find_id, 'domain': current_site.domain})
            msg = EmailMessage(subject="[SWAY 서비스] 아이디 찾기 메일", body=msg_html,
                               from_email="s340f914ss@gmail.com", to=[reg_email])
            msg.content_subtype = 'html'
            msg.send()
            return render(request, "accounts/find_id_success.html")
        except (ValueError):
            print("잘못된 값을 입력하였습니다.")

    return render(request, "accounts/find_id.html")

# 비밀번호 찾기 - email로 비밀번호를 변경하는 메일 발송


def find_password(request):
    if request.method == 'POST':
        try:
            email = request.POST.get('email')
            user = User.objects.filter(email__exact=email)
            user = user.values().get()
            print(user)
            register_email = user.values('email').get()

            reg_email = register_email['email']
            print(reg_email)

            # email로 아이디 전송
            current_site = get_current_site(request)

            msg_html = render_to_string('accounts/FindPW_Email.html',
                                        {'user': user,
                                         'domain': current_site.domain,
                                         'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                         'token': account_activation_token.make_token(user)})
            msg = EmailMessage(subject="[SWAY 서비스] 비밀번호 초기화 요청 메일", body=msg_html,
                               from_email="s340f914ss@gmail.com", to=[reg_email])
            msg.content_subtype = 'html'
            msg.send()
            return render(request, "accounts/find_password_process.html")
        except (TypeError, ValueError):
            print("비밀번호 변경 에러 발생")

    return render(request, "accounts/find_password.html")


def get_random_string(length):
    # Random string with the combination of lower and upper case
    letters = string.ascii_letters
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


def reset_password(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        print("uid : ", uid)
        user = User.objects.get(id=uid)
        print("user : ", user)
        print("pwd : ", user.password)
    except(TypeError, ValueError):
        user = None

    if user and account_activation_token.check_token(request.user, token):
        new_password = get_random_string(10)
        print(new_password)
        print("email : ", user.email)
        user.password = new_password
        user.save()
        msg_html = render_to_string('accounts/ResetPW_Email.html',
                                    {'password': new_password, 'domain': current_site.domain, })
        msg = EmailMessage(subject="[SWAY 서비스] 비밀번호 재설정 완료 메일", body=msg_html,
                           from_email="s340f914ss@gmail.com", to=[user.email])
        msg.content_subtype = 'html'
        msg.send()
        return render(request, "accounts/Reset_password_success.html")
    else:
        messages.error(request, "만료된 토큰입니다.")
        return render(request, "accounts/Reset_password_fail.html")
