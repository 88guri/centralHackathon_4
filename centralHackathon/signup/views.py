from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from .models import CustomUser
from character.models import Character
from .forms import LoginForm, SignUpForm
from django.contrib.auth.decorators import login_required


User = CustomUser

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            if request.session.get('verification_code') == request.POST.get('verification_code'):
                user = form.save()
                print(f"User saved: {user}")  # 디버깅: 저장된 사용자 정보 출력
                return redirect('login')
            else:
                form.add_error(None, '인증 코드가 잘못되었습니다.')
        else:
            print(form.errors)  # 디버깅: 폼 오류 출력
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def verify_code(request):
    if request.method == 'POST':
        input_code = request.POST.get('verification_code')
        if input_code and input_code == request.session.get('verification_code'):
            return JsonResponse({'message': '인증 성공'}, status=200)
        return JsonResponse({'error': '인증 코드가 잘못되었습니다.'}, status=400)
    return JsonResponse({'error': '잘못된 요청입니다.'}, status=400)


def signup_success(request):
    return render(request, 'Home.html')

def send_verification_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            verification_code = get_random_string(length=4, allowed_chars='0123456789')
            request.session['verification_code'] = verification_code

            send_mail(
                '[휴디] 인증 코드',
                f'인증번호: {verification_code}',
                'your_email@gmail.com',
                [email],
                fail_silently=False,
            )
            return JsonResponse({'message': '인증 코드가 이메일로 전송되었습니다.'}, status=200)
        else:
            return JsonResponse({'error': '이메일 주소를 입력해주세요.'}, status=400)
    else:
        return JsonResponse({'error': '잘못된 요청입니다.'}, status=400)

def verify_email(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('signup_success')
    else:
        form = SignUpForm()

    return render(request, 'verify_email.html', {'form': form})

def signup_success(request):
    return render(request, 'signup_success.html')

def join_page(request):
    form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def login_page(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home') 
            else:
                form.add_error(None, '유효하지 않은 이메일 또는 비밀번호입니다.')
    else:
        form = LoginForm()
    
    return render(request, 'Login.html', {'form': form})

def main_page(request):
    form = LoginForm()
    return render(request, 'Main.html', {'form': form})

@login_required
def home_page(request):
    try:
        character = Character.objects.get(user=request.user)
    except Character.DoesNotExist:
        return redirect('create_character')

    current_experience = character.experience
    max_experience = 1500

    context = {
        'character': character,
        'current_experience': current_experience,
        'max_experience': max_experience,
    }
    
    return render(request, 'Home.html', context)
