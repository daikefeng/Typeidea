from rest_framework import serializers, viewsets, pagination
from django.contrib.auth.models import User

from .models import Post, Category, Tag


#序列化
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('url', 'id', 'name', 'created_time',)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'id', 'username',)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('url', 'id', 'name', 'created_time',)



class PostSerializer(serializers.HyperlinkedModelSerializer):
    category = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
    )

    tags = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )

    owner = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    created_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = Post
        fields = ('url', 'title', 'desc', 'category', 'tags', 'pv', 'owner', 'created_time',)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = PostDetailSerializer
        return super(PostViewSet, self).retrieve(request, *args, **kwargs)




class PostDetailSerializer(serializers.HyperlinkedModelSerializer):
    category = CategorySerializer(
        read_only=True,
    )

    tags = TagSerializer(
        many=True,
        read_only=True,
    )

    owner = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Post
        fields = ('url', 'title', 'desc', 'category', 'tags', 'pv', 'owner', 'created_time',)


class TagDetailSerializer(serializers.ModelSerializer):
    #这里依赖于post,所以放到了PostView下面
    posts = serializers.SerializerMethodField('paginated_posts')

    def paginated_posts(self, obj):
        posts = obj.posts.all()
        paginator = pagination.PageNumberPagination()
        page = paginator.paginate_queryset(posts, self.context['request'])
        serializer = PostSerializer(page, many=True, context={'request': self.context['request']})
        return {
            'count': posts.count(),
            'previous': paginator.get_previous_link(),
            'next': paginator.get_next_link(),
            'results': serializer.data,
        }

    class Meta:
        model = Tag
        fields = ('url', 'id', 'name', 'created_time', 'posts',)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    #重写方法 获取详情页的时候指定为TagDetail类
    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = TagDetailSerializer
        return super(TagViewSet, self).retrieve(request, *args, **kwargs)


class UserDetailSerializer(serializers.ModelSerializer):
    post_set = PostSerializer(
        many=True,
        read_only=True,
    )
    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'post_set',)


class UserViewSet(viewsets.ModelViewSet):
    #这是用户列表
    queryset = User.objects.filter(is_staff=True)
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = UserDetailSerializer
        return super(UserViewSet, self).retrieve(request, *args, **kwargs)


class CategoryDetailSerializer(serializers.ModelSerializer):
    post_set = serializers.SerializerMethodField('paginated_posts')

    def paginated_posts(self, obj):
        post_set = obj.post_set.all()
        paginator = pagination.PageNumberPagination()
        page = paginator.paginate_queryset(post_set, self.context['request'])
        serializer = PostSerializer(page, many=True, context={'request': self.context['request']})
        return {
            'count': post_set.count(),
            'previous': paginator.get_previous_link(),
            'next': paginator.get_next_link(),
            'results': serializer.data,
        }
    class Meta:
        model = Category
        fields = ('url', 'id', 'name', 'created_time', 'post_set',)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.filter(status=1)
    serializer_class = CategorySerializer

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = CategoryDetailSerializer
        return super(CategoryViewSet, self).retrieve(request, *args, **kwargs)

