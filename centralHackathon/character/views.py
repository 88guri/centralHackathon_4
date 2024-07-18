from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Character
import json
import pytz
from datetime import datetime

@login_required
def home_page(request):
    character, created = Character.objects.get_or_create(user=request.user, defaults={'name': request.user.username})
    
    # 한국 표준 시간 설정
    KST = pytz.timezone('Asia/Seoul')
    now = datetime.now(KST)

    # 자정 초기화
    if now.hour == 1 and now.minute == 12:
        if character.last_elapsed_time > 0:
            experience_to_add = ((elapsed_time - character.last_elapsed_time) // 10) * 200
            character.add_experience(experience_to_add)
            character.last_elapsed_time = 0
            character.save()

    if request.method == 'POST':
        data = json.loads(request.body)
        elapsed_time = int(data.get('elapsed_time', 0))

        # 경험치 계산 및 업데이트
        experience_to_add = ((elapsed_time - character.last_elapsed_time) // 10) * 200
        character.add_experience(experience_to_add)
        character.last_elapsed_time = elapsed_time  # 마지막 타이머 시간 저장
        character.save()

        return JsonResponse({'experience': character.experience})

    return render(request, 'homee.html', {'character': character})