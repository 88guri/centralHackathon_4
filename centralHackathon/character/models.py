from django.db import models
from django.utils import timezone
from signup.models import CustomUser
from datetime import date

class Character(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    level = models.IntegerField(default=1)
    experience = models.IntegerField(default=0)
    stage = models.IntegerField(default=1)  # 총 3단계
    last_elapsed_time = models.IntegerField(default=0)  # 마지막 타이머 시간
    last_activity = models.DateTimeField(default=timezone.now) # 마지막 활동 시간을 추적 

    def add_experience(self, amount):
        self.experience += amount
        while self.experience >= 1000:
            self.experience -= 1000
            self.level_up()

    def level_up(self):
        self.level += 1
        if self.level % 8 == 0:
            self.evolve()

    def evolve(self):
        if self.stage < 3:
            self.stage += 1

    def __str__(self): 
        return f"{self.user.username}'s Character"

    def delete(self, *args, **kwargs):
        # 캐릭터와 관련된 UserItem을 삭제
        UserItem.objects.filter(user=self.user).delete()
        super().delete(*args, **kwargs)

class TimerLog(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateField(default=date.today)
    elapsed_time = models.IntegerField(default=0)

class Item(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='items/')
    
    def __str__(self):
        return self.name
    
class UserItem(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    acquired_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.item.name}"
