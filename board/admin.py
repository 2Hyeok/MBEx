from django.contrib import admin
from board.models import Board, ImageBoard

# Register your models here.
class BoardAdmin(admin.ModelAdmin):
    list_display = ("num", "writer", "subject", "passwd", "content", "readcount", "ref", "restep", "relevel", "regdate", "ip")
    
admin.site.register(Board, BoardAdmin)

class ImageAdmin(admin.ModelAdmin):
    list_display=("title", "photo")

admin.site.register(ImageBoard, ImageAdmin)