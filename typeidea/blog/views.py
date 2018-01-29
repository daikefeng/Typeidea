from django.conf import settings
from django.core.cache import cache
from django.views.generic import ListView, DetailView
from django.db.models import F

import logging

from .models import Post, Tag, Category
from config.models import SideBar
from comment.models import Comment
from comment.forms import CommentForm


logger = logging.getLogger(__name__)

class CommonMixin(object):
    #自己定义一个方法， 这是为了让每个方法变的更小，从而实现根据不同的需求实现定制
    def get_category_context(self):
        categories = Category.objects.filter(status=1)
        nav_cates = []
        cates = []
        for cate in categories:
            if cate.is_nav:
                nav_cates.append(cate)
            else:
                cates.append(cate)
        return {
            'nav_cates': nav_cates,
            'cates': cates
        }
    #用来渲染模版,跟get_queryset()一样是django自己的方法
    def get_context_data(self, **kwargs):
        side_bars = SideBar.objects.filter(status=1)
        recently_posts = Post.objects.filter(status=1)[:10]
        recently_comments = Comment.objects.filter(status=1)[:10]
        hot_posts = Post.objects.filter(status=1).order_by('-pv')[:10]
        kwargs.update({
            'side_bars': side_bars,
            'recently_posts': recently_posts,
            'recently_comments': recently_comments,
            'footer_name': 'power by daikefeng',
            'hot_posts': hot_posts,
        })
        kwargs.update(self.get_category_context())
        #get_context_data会把里面的参数字段直接暴露在模版中
        return super(CommonMixin, self).get_context_data(**kwargs)


#抽象出来一个基类
class BasePostView(CommonMixin, ListView):
    model = Post
    template_name = 'blog/list.html'
    context_object_name = 'posts'
    paginate_by = 3


class IndexView(BasePostView):
    def get_queryset(self):
        query = self.request.GET.get('query')
        logger.info('query: [%s]', query)
        qs = super(IndexView, self).get_queryset()
        if query:
            #qs是传给了context_object_name
            qs = qs.filter(title__icontains=query)
        logger.info('query result: [%s]', qs)
        return qs


    def get_context_data(self, **kwargs):
        query = self.request.GET.get('query')
        return super(IndexView, self).get_context_data(query=query)


class CategoryView(BasePostView):
    #重写get_query()方法
    def get_queryset(self):
        qs = super(CategoryView, self).get_queryset()
        #kwargs.get()是用来获取url中有参数命名的数据，一般来说都是用request.GET.get('xxx')
        cate_id = self.kwargs.get('category_id')
        qs = qs.filter(category_id=cate_id)
        #qs 就是传给了get_context_data()方法,对应context_object_name这个变量名
        return qs


class TagView(BasePostView):
    def get_queryset(self):
        tag_id = self.kwargs['tag_id']
        try:
            tag = Tag.objects.get(id=tag_id)
        except Tag.DoesNotExist:
            return []

        qs = tag.posts.all()
        return qs


class PostView(CommonMixin, DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get_comments(self):
        target = self.request.path
        comments = Comment.objects.filter(target=target)
        return comments

    #渲染评论表单到detail页面中
    def get_context_data(self, **kwargs):
        kwargs.update({
            'comment_form': CommentForm(),
            'comment_list': self.get_comments()
        })
        return super(PostView, self).get_context_data(**kwargs)

    def get(self, request, *args, **kwargs):
        response = super(PostView, self).get(request, *args, **kwargs)
        self.pv_uv()
        return response

    def pv_uv(self):
        #业务逻辑放到view层来处理
        sessionid = self.request.COOKIES.get('sessionid')
        if not sessionid:
            return

        pv_key = 'uv: %s: %s' % (sessionid, self.request.path)
        if not cache.get(pv_key):
            self.object.increase_pv()
            cache.set(pv_key, 1, 30)

        uv_key = 'uv: %s: %s'%(sessionid, self.request.path)
        if not cache.get(uv_key):
            self.object.increase_uv()
            cache.set(uv_key, 1, 60*60*24)


class AuthorView(BasePostView):
    def get_queryset(self):
        author_id = self.kwargs['author_id']
        qs = super(AuthorView, self).get_queryset()
        if author_id:
            qs = qs.filter(owner_id=author_id)
        return qs
