from rest_framework import generics
from blog.models import Post
from blog.serializers import PostSerializer


class PostListView(generics.ListCreateAPIView):
    queryset = Post.published.all()
    serializer_class = PostSerializer


class PostDetailView(generics.RetrieveDestroyAPIView):
    queryset = Post.published.all()
    serializer_class = PostSerializer
