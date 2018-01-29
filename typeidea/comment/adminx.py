import xadmin
from .models import Comment
from typeidea.adminx import BaseOwnerAdmin


class CommentAdmin(BaseOwnerAdmin):
    list_display = ['target', 'nickname', 'website', 'email', 'created_time']


xadmin.site.register(Comment, CommentAdmin)