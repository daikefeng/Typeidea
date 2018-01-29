from django.views.generic import ListView

from blog.views import CommonMixin
from .models import Link
from comment.views import CommentShowMixin
from comment.models import Comment
from comment.forms import CommentForm


class LinkView(CommonMixin, ListView, CommentShowMixin):
    queryset = Link.objects.filter(status=1)
    template_name = 'config/links.html'
    context_object_name = 'links'

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
        return super(LinkView, self).get_context_data(**kwargs)
