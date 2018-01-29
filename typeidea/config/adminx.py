import xadmin

from .models import Link, SideBar
from typeidea.adminx import BaseOwnerAdmin


class LinkAdmin(BaseOwnerAdmin):
    exclude = ['owner']


class SideBarAdmin(BaseOwnerAdmin):
    exclude = ['owner']


xadmin.site.register(Link, LinkAdmin)
xadmin.site.register(SideBar,  SideBarAdmin)

