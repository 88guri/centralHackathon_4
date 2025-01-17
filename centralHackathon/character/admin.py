from django.contrib import admin
from .models import Character, Item

class CharacterAdmin(admin.ModelAdmin):
    list_display = ('name', 'level', 'experience')

admin.site.register(Character, CharacterAdmin) #이상하게 admin에 캐릭터 필드가 안뜨길래 추가했어요-시현

class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'image')

admin.site.register(Item, ItemAdmin)