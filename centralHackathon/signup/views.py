from django.shortcuts import render, redirect
from .forms import SignUpForm, LoginForm 
from django.contrib.auth import authenticate, login #추가한 부분
 
'''
def save(self, *args, **kwargs):
        if not self.pk:
            self.username = self.email
        super().save(*args, **kwargs)'''

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            #print("valid")
            form.save()
            return redirect('signup_success')
        else:
            #print("notvalid")
            return render(request, 'signup.html', {'form':form})
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form':form})

def signup_success(request):
    return render(request, 'signup_success.html')

def join_page(request):
    form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def login_page(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)  
        if form.is_valid():
            username = form.cleaned_data['username']  # 사용자가 입력한 ID(이메일)를 가져옴
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                # 로그인 성공
                login(request, user)
                return redirect('home')
            else:
                # 로그인 실패
                print("로그인 실패")
                pass
    else:
        form = LoginForm()  
    return render(request, 'Login.html', {'form': form})

def main_page(request):
    form = LoginForm()
    return render(request, 'Main.html', {'form': form})

def home_page(request):
    return render(request, 'Home.html')