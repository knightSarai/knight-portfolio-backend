from rest_framework import generics
from blog.models import Post
from blog.serializers import PostSerializer

class PostListView(generics.ListAPIView):
    queryset = Post.published.all()
    serializer_class = PostSerializer


class PostDetailView(generics.RetrieveAPIView):
    queryset = Post.published.all()
    serializer_class = PostSerializer
