from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.template import loader
from django.http.response import HttpResponse
from board.models import Board
import logging
from django.utils.dateformat import DateFormat
from datetime import datetime
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

logger = logging.getLogger(__name__) # 로거표시

PAGE_SIZE = 5 # 한페이지에 5개의 글
PAGE_BLOCK = 3  # 넘어가는것 3개


# 리스트
class ListView( View ) :
    def get(self, request ) :
        template = loader.get_template( "list.html" )
        count = Board.objects.all().count() # 글 전체의 갯수, Board에 있는 count
        
        pagenum = request.GET.get( "pagenum" ) # 페이지num
        if not pagenum :
            pagenum = "1"
        
        pagenum = int( pagenum ) # 페이지num 을 보겠다
        
        # 한 페이지에 몇개씩 표기하겠다를 정해주어야함
        start = ( pagenum - 1 ) * int(PAGE_SIZE)        # ( 5 - 1 ) * 10  + 1    41
        end = start + int(PAGE_SIZE) - 1                # 41 + 10 - 1            50
        if end > count :
            end = count
        
        # 리스트임
        dtos = Board.objects.order_by( "-ref", "restep" )[start:end+1] # 같은 그룹이면서, 나중에 쓴 글을올려야함, ref를 내림차순, restep을 오름차순으로 정렬
                                                                    # 슬라이싱이 -1이라 글을 하나 적게 가져옴
                                                                    # start 부터 end 까지 잘라서 가져와라
                                                                  
        # 글번호 출력도 계산해야함                                                
        number = count - ( pagenum - 1 ) * int(PAGE_SIZE)
        
        # 페이지 넘기기
        startpage = pagenum // int(PAGE_BLOCK) * int(PAGE_BLOCK) + 1      # 9 // 10 * 10 + 1    1
        if pagenum % int(PAGE_BLOCK) == 0 :
            startpage -= int(PAGE_BLOCK) # 페이지 고정
        endpage = startpage + int(PAGE_BLOCK) - 1                         # 1 + 10 -1           10
        pagecount = count // int(PAGE_SIZE)
        if count % int(PAGE_SIZE) > 0 :
            pagecount += 1
        if endpage > pagecount :
            endpage = pagecount  
        pages = range( startpage, endpage+1 )    
        context = {
            "count" : count,
            "dtos" : dtos,
            "pagenum" : pagenum,
            "number" : number,
            "pages" : pages,
            "startpage" : startpage,
            "endpage" : endpage,
            "pageblock" : PAGE_BLOCK,
            "pagecount" : pagecount,
            }
        return HttpResponse( template.render( context, request ) )
    def post(self, request ) :
        pass
    

# 글 작성
class WriteView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(WriteView, self ).dispatch( request, *args, **kwargs )
    
    def get(self,request):
        ref=1
        restep=0
        relevel=0
        # num=request.GET["num"] 에러발생
        # 받는것이 두가지방법이있음
        num = request.GET.get("num") # 예외 하나가 자동으로 잡힘, 보통은 이렇게 잡음 에러방지를 위해 받기도함
        if num == None :
            # 제목글 이라는뜻
            try : # 글이 있는경우
                maxnum = Board.objects.order_by("-num").values()[0]["num"] # num으로 내림차순 정렬, 맨 위의 것
                ref = maxnum + 1        # 그룹화 아이디 글번호 최대값 + 1
                
            except IndexError:
                # 글이 없는 경우
                ref = 1
                
        else :
            # 답변글 이라는뜻
            # 나중에 쓴 답글은 위로 올라가야함
            # ref = request.GET["ref"]
            # restep = request.GET["restep"]
            # relevel = request.GET["relevel"]
            ref = request.GET["ref"]
            restep = request.GET["restep"]
            relevel = request.GET["relevel"]
            res = Board.objects.filter( restep__gt=restep and ref==ref) # gt, 크냐로 들어감 get, 순서 중요
            for re in res :
                re.restep = int(re.restep + 1) # 원레는 +1 해주면 되는데 자료형이 안넘어와 강제 형변환필요
                re.save()
            
            restep = int(restep) + 1
            relevel = int(relevel) + 1
        
        # write 폼으로 넘어갔다가 다시 post로 넘어감
        template = loader.get_template( "writearticle.html" )
        context = {
            "num" : num,
            "ref" : ref,
            "restep" : restep,
            "relevel" : relevel,
            }
        return HttpResponse( template.render( context, request ) )
    
    def post(self,request):
        dto = Board(
            writer = request.POST["writer"],
            subject = request.POST["subject"],
            passwd = request.POST["passwd"],
            content = request.POST["content"],
            readcount = 0, # 이건 없어도됨
            ref = request.POST["ref"],
            restep = request.POST["restep"],
            relevel = request.POST["relevel"],
            regdate = DateFormat(datetime.now()).format("Ymd"),
            ip = request.META.get("REMOTE_ADDR")
            )
        dto.save()
        return redirect("board:list")
    
# 글 보기
class DetailView(View):
    def get(self,request):
        num = request.GET["num"]
        pagenum = request.GET["pagenum"]
        number = request.GET["number"]
        dto = Board.objects.get(num=num)
        if dto.ip != request.META.get("REMOTE_ADDR") : # 현재 접속중인 아이피와 디비의 아이피 비교
            dto.readcount += 1
            dto.save()
        context = {
            "num" : num,
            "pagenum" : pagenum,
            "number" : number,
            "dto" : dto,
            }
        template = loader.get_template("detailarticle.html")
        return HttpResponse(template.render(context,request))
    
    def post(self,request):
        pass