from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Character
from .forms import CharacterForm
from datetime import datetime
import json, pytz

@login_required
def create_character(request):
    if request.method == 'POST':
        form = CharacterForm(request.POST)
        if form.is_valid():
            character = form.save(commit=False)
            character.user = request.user
            character.save()
            return redirect('timer_page')
    else:
        form = CharacterForm()
    return render(request, 'create_character.html', {'form': form})


@login_required
def timer_page(request):
    try:
        character = Character.objects.get(user=request.user)
    except Character.DoesNotExist:
        return redirect('create_character')
    
    # 한국 표준 시간 설정
    KST = pytz.timezone('Asia/Seoul')
    now = datetime.now(KST)

    # 자정 초기화 (테스트를 위해 임시로 자정 설정 X)
    if now.hour == 18 and now.minute == 6 and now.second == 0:
        data = json.loads(request.body)
        elapsed_time = int(data.get('elapsed_time', 0))

        # 경험치 계산 및 업데이트
        if character.last_elapsed_time > 0:
            experience_to_add = ((elapsed_time - character.last_elapsed_time) // 10) * 200
        else:
            experience_to_add = (elapsed_time // 10) * 200

        character.add_experience(experience_to_add)
        character.last_elapsed_time = 0
        character.save()

        return JsonResponse({'experience': character.experience, 'elapsed_time': character.last_elapsed_time})

    if request.method == 'POST':
        data = json.loads(request.body)
        elapsed_time = int(data.get('elapsed_time', 0))

        # 경험치 계산 및 업데이트
        experience_to_add = ((elapsed_time - character.last_elapsed_time) // 10) * 200
        character.add_experience(experience_to_add)
        character.last_elapsed_time = elapsed_time  # 마지막 타이머 시간 저장
        character.save()

        return JsonResponse({'experience': character.experience})

    return render(request, 'timer.html', {'character': character})