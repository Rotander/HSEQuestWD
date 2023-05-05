from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from user.models import ErrorReport, Game, Present, User

admin.site.register(User, UserAdmin)
admin.site.register(Game)
admin.site.register(Present)
admin.site.register(ErrorReport)
