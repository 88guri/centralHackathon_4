from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Sum
from .models import Character, TimerLog, Item, UserItem
from .forms import CharacterForm
from datetime import datetime, timedelta
import json, pytz, random

# 사용자 비활성화 확인하는거!
def check_inactivity(character): 
    now = timezone.now() 
    if character.last_activity:
        if now - character.last_activity > timedelta(days=3):
            return True 
    return False 

@login_required
def create_character(request):
    if request.method == 'POST':
        form = CharacterForm(request.POST)
        if form.is_valid():
            character = form.save(commit=False)
            character.user = request.user
            character.save()
            return redirect('home')
    else:
        form = CharacterForm()
    return render(request, 'create_character.html', {'form': form})

@login_required
def timer_page(request):
    try:
        character = Character.objects.get(user=request.user)
    except Character.DoesNotExist:
        return redirect('create_character')
    
    if check_inactivity(character):  
        return redirect('character_missing') 

    # 한국 표준 시간 설정
    KST = pytz.timezone('Asia/Seoul')
    now = datetime.now(KST)

    # 자정 초기화
    if now.hour == 0 and now.minute == 0 and now.second == 0:
        if request.method == 'POST':
            data = json.loads(request.body)
            elapsed_time = int(data.get('elapsed_time', 0))

            # 타이머 로그 저장
            timer_log, created = TimerLog.objects.get_or_create(user=request.user, date=now.date())
            timer_log.elapsed_time += elapsed_time - character.last_elapsed_time
            timer_log.save()

            time = elapsed_time - character.last_elapsed_time

            hours = time // 3600
            minutes = (time % 3600) // 60
            seconds = time % 60

            # 경험치 계산 및 업데이트
            if character.last_elapsed_time > 0:
                experience_to_add = elapsed_time - character.last_elapsed_time
            else:
                experience_to_add = elapsed_time

            character.add_experience(experience_to_add)
            character.last_elapsed_time = 0
            character.last_activity = now  # 마지막 활동 시간 갱신 
            character.save()

            return JsonResponse({
                'experience': experience_to_add, 
                'elapsed_time': character.last_elapsed_time,
                'hours': hours,
                'minutes': minutes,
                'seconds': seconds,
                'level': character.level,
                'stage': character.stage,
                'reward_eligible': time >= 5,
            })

    if request.method == 'POST':
        data = json.loads(request.body)
        elapsed_time = int(data.get('elapsed_time', 0))

        # 타이머 로그 저장
        timer_log, created = TimerLog.objects.get_or_create(user=request.user, date=now.date())
        timer_log.elapsed_time += elapsed_time - character.last_elapsed_time
        timer_log.save()

        time = elapsed_time - character.last_elapsed_time

        hours = time // 3600
        minutes = (time % 3600) // 60
        seconds = time % 60

        # 경험치 계산 및 업데이트
        experience_to_add = elapsed_time - character.last_elapsed_time
        character.add_experience(experience_to_add)
        character.last_elapsed_time = elapsed_time  # 마지막 타이머 시간 저장
        character.last_activity = now  # 마지막 활동 시간 갱신 
        character.save()

        # 디버그용 로그
        print(f"Calculated Time: {time}")
        print(f"Hours: {hours}, Minutes: {minutes}, Seconds: {seconds}")

        return JsonResponse({
            'experience': experience_to_add,
            'hours': hours,
            'minutes': minutes,
            'seconds': seconds,
            'level': character.level,
            'stage': character.stage,
            'reward_eligible': time >= 5,
        })

    # 마지막 활동 시간 갱신 
    character.last_activity = now 
    character.save() 

    # 캐릭터의 이름을 timer.html에 전달 
    context = {
        'character': character,
        'character_name': character.name  
    }
    
    return render(request, 'timer.html', context)


@login_required
def claim_reward(request):
    if request.method == 'POST':
        user = request.user
        items = list(Item.objects.all())
        if items:
            item_reward = random.choice(items)
            UserItem.objects.create(user=user, item=item_reward)
            print(f"image: {item_reward.image.url}")
            return JsonResponse({
                'item': item_reward.name, 
                'image': item_reward.image.url
                })
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def watch_ad_reward(request): 
    if request.method == 'POST':
        user = request.user
        items = list(Item.objects.all())
        if items:
            item_rewards = random.sample(items, 2)  # 아이템 2개 랜덤 선택
            for item_reward in item_rewards:
                UserItem.objects.create(user=user, item=item_reward)
            # 첫 번째 아이템 정보
            first_item = item_rewards[0]
            return JsonResponse({
                'item_name': first_item.name, 
                'item_image': first_item.image.url
            })
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def character_missing(request):
    try:
        # 사용자로부터 캐릭터를 가져옴
        character = Character.objects.get(user=request.user)
        character_name = character.name
        character_level = character.level  # 캐릭터 레벨 추가
    except Character.DoesNotExist:
        character_name = None
        character_level = None  # 캐릭터가 없을 경우 기본 값 설정

    if request.method == 'POST': 
        # 광고 시청 후 캐릭터 복구
        return redirect('watch_ad') 

    # 템플릿에 캐릭터 이름과 레벨을 전달
    return render(request, 'character_missing.html', {
        'character_name': character_name,
        'character_level': character_level  # 레벨을 템플릿 컨텍스트에 추가
    })

# 광고 - 가출
@login_required
def watch_ad(request): 
    if request.method == 'POST': 
        # 광고 시청 완료 후 캐릭터 복구
        character = Character.objects.get(user=request.user) 
        character.last_activity = timezone.now()  # 캐릭터 복구할 때  활동 시간 갱신 
        character.save() 
        return redirect('timer_page') 
    return render(request, 'watch_ad.html')

# 광고 - 2배 보상
@login_required
def watch_ad2(request): 
    if request.method == 'POST':
        try:
            character = Character.objects.get(user=request.user)
        except Character.DoesNotExist:
            return redirect('create_character')
        item_name = request.POST.get('item_name')
        item_image = request.POST.get('item_image')
        return render(request, 'watch_ad2.html', {
            'character_name': character.name,
            'item_name': item_name,
            'item_image': item_image
        })
    return render(request, 'watch_ad2.html')

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

    # 오늘 포함 지난 4일의 집중 시간 계산
    dates = [now - timedelta(days=i) for i in range(4)]
    logs = {}
    for date in dates:
        timer_log = TimerLog.objects.filter(user=request.user, date=date).first()
        elapsed_time = timer_log.elapsed_time if timer_log else 0
        hours = elapsed_time // 3600
        minutes = (elapsed_time % 3600) // 60
        seconds = elapsed_time % 60
        logs[date] = {'hours': hours, 'minutes': minutes, 'seconds': seconds}

    # 오늘 제외 지난 7일의 일일 평균 계산
    last_7_days = [now - timedelta(days=i) for i in range(1, 8)]
    total_time_last_7_days = sum(TimerLog.objects.filter(user=request.user, date=date).aggregate(total_time=Sum('elapsed_time'))['total_time'] or 0 for date in last_7_days)
    average_time_last_7_days = total_time_last_7_days / 7 if total_time_last_7_days else 0

    # 지난주 대비 집중 시간 계산
    last_week_date = now - timedelta(days=7)
    last_week_log = TimerLog.objects.filter(user=request.user, date=last_week_date).first()
    last_week_time = last_week_log.elapsed_time if last_week_log else None

    today_log = TimerLog.objects.filter(user=request.user, date=now).first()
    today_time = today_log.elapsed_time if today_log else 0

    if last_week_time is not None:
        if last_week_time > 0:
            percentage_change = ((today_time - last_week_time) / last_week_time) * 100
        else:
            percentage_change = 0 if today_time == 0 else 100
        percentage_change_str = f"{percentage_change:.0f}"
    else:
        percentage_change_str = "지난주의 데이터가 존재하지 않습니다."

    avg_hours = int(average_time_last_7_days // 3600)
    avg_minutes = int((average_time_last_7_days % 3600) // 60)
    avg_seconds = int(average_time_last_7_days % 60)

    context = {
        'logs': logs,
        'avg_hours': avg_hours,
        'avg_minutes': avg_minutes,
        'avg_seconds': avg_seconds,
        'percentage_change': percentage_change_str
    }

    return render(request, 'detailed_history.html', context)

@login_required
def deco(request):
    try:
        character = Character.objects.get(user=request.user)
    except Character.DoesNotExist:
        return redirect('character_lost_forever') 
    
    # 유저 아이템을 가져옴
    all_user_items = UserItem.objects.filter(user=request.user).order_by('acquired_date')

    # 아이템 이름 기준으로 중복 제거
    unique_user_items = []
    seen_items = set()
    for item in all_user_items:
        if item.item.name not in seen_items:
            seen_items.add(item.item.name)
            unique_user_items.append(item)

    context = {
        'user_items': unique_user_items,
        'character': character,
    }
    return render(request, 'deco.html', context)


@login_required
def character_lost_forever(request):
    try:
        character = Character.objects.get(user=request.user)
        # 캐릭터와 관련된 UserItem을 삭제
        UserItem.objects.filter(user=request.user).delete()
        character.delete()
    except Character.DoesNotExist:
        pass  # 캐릭터가 존재하지 않을 경우 처리

    return render(request, 'character_lost_forever.html')
