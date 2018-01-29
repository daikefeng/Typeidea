import xadmin
from django.urls import reverse
from django.utils.html import format_html
from xadmin.layout import Fieldset, Row

from .models import Post, Category, Tag
from .adminforms import PostAdminForm
from typeidea.adminx import BaseOwnerAdmin


class PostAdmin(BaseOwnerAdmin):
    form = PostAdminForm

    list_display = ['title', 'category', 'status', 'pv', 'uv', 'owner', 'created_time', 'operator']
    list_filter = ['category', 'owner']
    search_fields = ['title', 'category__name']
    save_on_top = True
    actions_on_top = True
    actions_on_bottom = True
    exclude = ('html', 'owner', 'pv', 'uv')

    form_layout = (
        Fieldset(
            '基础信息',
            'title',
            'desc',
            Row('category', 'status', 'is_markdown'),
            'content',
            'tags',
        ),
    )

    def operator(self, obj):
        return format_html(
            '<a href={}>编辑</a>',
            reverse('cus_admin:blog_post_change', args=(obj.id,))
        )
    operator.allow_tags = True
    operator.short_description = '操作'


class CategoryAdmin(BaseOwnerAdmin):
    list_display = ['name', 'status', 'is_nav', 'created_time']
    fields = (
        'name', 'status',
        'is_nav',
    )


class TagAdmin(BaseOwnerAdmin):
    list_display = ['name', 'status', 'created_time']
    fields = (
        'name', 'status',
    )


xadmin.site.register(Post, PostAdmin)
xadmin.site.register(Category, CategoryAdmin)
xadmin.site.register(Tag, TagAdmin)