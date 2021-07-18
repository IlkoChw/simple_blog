from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import UserProfile, Post


class UserInline(admin.StackedInline):
    model = UserProfile
    can_delete = False


class UserAdmin(UserAdmin):
    inlines = (UserInline, )


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('__str__', )


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
