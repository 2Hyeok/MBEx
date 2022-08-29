from django.db import models
from member.choice import DEPART_CHOICE

# Create your models here.

class Member(models.Model):
    id = models.CharField(max_length=50, verbose_name="아이디", primary_key=True) # verbose -> 마우스 올렸을시 보이는 이름
    passwd = models.CharField(max_length=50, verbose_name="비밀번호", null=False)
    name = models.CharField(max_length=50, verbose_name="이름", null=False)
    email = models.CharField(max_length=100, verbose_name="이메일", null=True)
    tel = models.CharField(max_length=30, verbose_name="전화번호", null=True)
    depart = models.CharField(choices=DEPART_CHOICE, max_length=50, verbose_name="부서", null=False) # depart_choice 없음, 만들어 주어야함
    logtime = models.DateTimeField(auto_now_add=True, verbose_name="가입일", null=False, blank=True)