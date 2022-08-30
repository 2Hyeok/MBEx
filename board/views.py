from django.shortcuts import render
from django.views.generic.base import View
from django.template import loader
from django.http.response import HttpResponse
from board.models import Board
import logging

# Create your views here.

logger = logging.getLogger(__name__) # 로거표시

class ListView(View):
    def get(self,request):
        template = loader.get_template("list.html")
        count = Board.objects.all().count() # 글 전체의 갯수, Board에 있는 count
        context = {
            "count" : count
            }
        return HttpResponse(template.render(context,request))

    def post(self,request):
        pass
    
class WirteView(View):
    def get(self,request):
        template = loader.get_template("writearticle.html")
        context = {}
        return HttpResponse(template.render(context,request))
    
    def post(self,request):
        pass