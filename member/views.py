from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.template import loader
from django.http.response import HttpResponse


import logging
from member.models import Member
from django.utils.dateformat import DateFormat
from datetime import datetime
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
logger = logging.getLogger(__name__) # 로거 추가
# 프로젝트 폴더 밑 log 라는 패키지 안에 생성

# Create your views here.

# 메인페이지
class MainView( View ) :
    def get(self, request ) :
        memid = request.session.get( "memid" )
        if memid : # 아이디가 있을시
            context = {
                "memid" : memid,
                }
        else : # 아이디가 없을시
            context = {}
        template = loader.get_template( "main.html" )
        return HttpResponse( template.render( context, request ) )
    def post(self, request ) :
        pass


# 아이디 중복확인
class ConfirmView(View):
    # 둘다 get 방식으로 넘길경우 csrf token이 필요 없음
    # @method_decorator( csrf_exempt )
    # def dispatch( self, request, *args, **kwargs ) :
    #     return super( WriteView, self ).dispatch( request, *args, **kwargs )
    
    def get(self,request):
        id = request.GET["id"]
        result = 0
        try :
            Member.objects.get(id=id)
            result = 1
        except ObjectDoesNotExist :
            result = 0
        context = {
            "result" : result,
            "id" : id
            }
        logger.info("id : " + id)
        template = loader.get_template("confirm.html")
        return HttpResponse(template.render(context,request))
            
    def post(self,request):
        pass # 아예 안쓸것 이기에 pass로 처리

# 회원가입
class WriteView( View ):
    @method_decorator( csrf_exempt )
    def dispatch( self, request, *args, **kwargs ) :
        return super( WriteView, self ).dispatch( request, *args, **kwargs )
    
    def get(self, request ) :
        template = loader.get_template( "write.html" )
        context = {}
        return HttpResponse( template.render( context, request ) )
        
    def post(self,request):
        # 가입한 아이디를 넣어줌
        # 쓸대없는 데이터까지 넣어야함
        tel = ""
        tel1 = request.POST["tel1"]
        tel2 = request.POST["tel2"]
        tel3 = request.POST["tel3"]
        if tel1 and tel2 and tel3 :
            tel = tel1 + "-" + tel2 + "-" + tel3
            
        dto = Member(
            id = request.POST["id"],
            passwd = request.POST["passwd"],
            name = request.POST["name"],
            email = request.POST["email"],
            tel = tel,
            depart = request.POST["depart"],
            logtime = DateFormat( datetime.now() ).format( "Y-m-d" )            
            )
        dto.save()
        logger.info("writer : " + str(id)) # 문자열로 형변환을 해주어야함, 회원가입시 해당 아이디를 로그에 저장
        # 저장을 무엇으로 할지 정해야함, logger, info, error, critical 등 함수로 잡아야함, 가입한 아이디만 표시
        # 세팅에 info 밑에만 잡게 되어있기에 info로 잡아야함
        # 문자열 하나만 넘어가게 되어있어서 , 가아닌 +를 주어야함
        return redirect("login")

# 로그인 처리
class LoginView( View ) :
    @method_decorator( csrf_exempt )
    def dispatch( self, request, *args, **kwargs ) :
        return super( LoginView, self ).dispatch( request, *args, **kwargs )
    def get(self, request ) :
        template = loader.get_template( "login.html" )
        context = {}
        return HttpResponse( template.render( context, request ) )
    def post(self, request ) :
        id = request.POST["id"]
        passwd = request.POST["passwd"]
        try :
            dto = Member.objects.get( id=id )
            if passwd == dto.passwd :
                request.session["memid"] = id
                return redirect( "main" )
            else :
                message = "비밀번호가 다릅니다"            
        except ObjectDoesNotExist :
            message = "아이디가 없습니다"
        template = loader.get_template( "login.html" )
        context = {
            "message" : message, 
            }   
        return HttpResponse( template.render( context, request ) )