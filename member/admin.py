from django.contrib import admin
from member.models import Member

# Register your models here.
class MemberAdmin(admin.ModelAdmin):
    list_display = ("id", "passwd", "name", "email", "tel", "depart")

admin.site.register(Member, MemberAdmin)