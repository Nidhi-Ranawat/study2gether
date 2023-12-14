from django.contrib import admin
from .models import Room, Topic, Messages, User
# Register your models here.

admin.site.register(User)
# no need to register User model unless created our own
admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Messages)
