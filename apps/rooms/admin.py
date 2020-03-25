from django.contrib import admin
from .models import Room, Message


class MessageInline(admin.TabularInline):
    model = Message


class RoomModelAdmin(admin.ModelAdmin):
    list_display = 'title', 'created_by', 'is_private'
    inlines = [MessageInline]


admin.site.register(Room, RoomModelAdmin)
