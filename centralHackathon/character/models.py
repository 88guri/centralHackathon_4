from django.db import models
from signup.models import CustomUser

class Character(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    level = models.IntegerField(default=1)
    experience = models.IntegerField(default=0)
    stage = models.IntegerField(default=1)  # 총 3단계
    last_elapsed_time = models.IntegerField(default=0)  # 마지막 타이머 시간

    def add_experience(self, amount):
        self.experience += amount
        while self.experience >= 2000:
            self.experience -= 2000
            self.level_up()

    def level_up(self):
        self.level += 1
        if self.level % 25 == 0:
            self.evolve()

    def evolve(self):
        if self.stage < 3:
            self.stage += 1
