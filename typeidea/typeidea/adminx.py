import xadmin
from xadmin.views import CommAdminView


class BaseOwnerAdmin(object):
    # 重写save_model - 保证每条数据都属于当前用户
    # 重写get_queryset - 保证每个用户只能看到自己的文章

    def get_list_queryset(self):
        request = self.request
        qs = super(BaseOwnerAdmin, self).get_list_queryset()
        if request.user.is_superuser:
            return qs
        return qs.filter(owner=request.user)

    def save_models(self):
        if self.org_obj:
            return super(BaseOwnerAdmin, self).save_models()
        self.new_obj.owner = self.request.user
        return super(BaseOwnerAdmin, self).save_models()


class GlobalSetting(object):
    title = 'Typeidea管理后台'
    footer = '@ power by daikefeng.com'

xadmin.site.register(CommAdminView, GlobalSetting)

