from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Character, TimerLog
from .forms import CharacterForm
from datetime import datetime, timedelta
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
    if now.hour == 23 and now.minute == 59 and now.second == 0:
        data = json.loads(request.body)
        elapsed_time = int(data.get('elapsed_time', 0))

        # 타이머 로그 저장
        timer_log, created = TimerLog.objects.get_or_create(user=request.user, date=now.date())
        timer_log.elapsed_time += elapsed_time - character.last_elapsed_time
        timer_log.save()

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

        # 타이머 로그 저장
        timer_log, created = TimerLog.objects.get_or_create(user=request.user, date=now.date())
        timer_log.elapsed_time += elapsed_time - character.last_elapsed_time
        timer_log.save()

        # 경험치 계산 및 업데이트
        experience_to_add = ((elapsed_time - character.last_elapsed_time) // 10) * 200
        character.add_experience(experience_to_add)
        character.last_elapsed_time = elapsed_time  # 마지막 타이머 시간 저장
        character.save()

        return JsonResponse({'experience': character.experience})

    return render(request, 'timer.html', {'character': character})

@login_required
def history_page(request):
    logs = TimerLog.objects.filter(user=request.user).order_by('-date')

    total_time = sum(log.elapsed_time for log in logs)

    # 연속 집중 일수 계산
    consecutive_days = 0
    if logs:
        consecutive_days = 1
        previous_day = logs[0].date
        for log in logs[1:]:
            if previous_day - log.date == timedelta(days=1):
                consecutive_days += 1
            else:
                break
            previous_day = log.date

    total_hours = total_time // 3600
    total_minutes = (total_time % 3600) // 60
    total_seconds = total_time % 60

    return render(request, 'history.html', {
        'total_hours': total_hours,
        'total_minutes': total_minutes,
        'total_seconds': total_seconds,
        'consecutive_days': consecutive_days,
        'logs': logs,
    })

@login_required
def detailed_history(request):
    # 한국 표준 시간 설정
    KST = pytz.timezone('Asia/Seoul')
    now = datetime.now(KST).date()

    # 최근 4일의 날짜
    dates = [now - timedelta(days=i) for i in range(4)]

    # 각 날짜에 해당하는 타이머 로그
    logs = {}
    for date in dates:
        timer_log = TimerLog.objects.filter(user=request.user, date=date).first()
        elapsed_time = timer_log.elapsed_time if timer_log else 0
        hours = elapsed_time // 3600
        minutes = (elapsed_time % 3600) // 60
        seconds = elapsed_time % 60
        logs[date] = {'hours': hours, 'minutes': minutes, 'seconds': seconds}

    context = {
        'logs': logs
    }

    return render(request, 'detailed_history.html', context)