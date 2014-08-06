from snippets.models import Snippet
from snippets.serializers import SnippetSerializer, UserSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework import permissions
from snippets.permissions import IsOwnerOrReadOnly
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework import renderers


@api_view(('GET',))
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'snippets': reverse('snippet-list', request=request, format=format)
    })


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer




#class SnippetList(APIView):
#    """
#    List all snippets, or create a new snippet.
#    """
#    def get(self, request, format=None):
#        snippets = Snippet.objects.all()
#        serializer = SnippetSerializer(snippets, many=True)
#        return Response(serializer.data)
#
#    def post(self, request, format=None):
#        serializer = SnippetSerializer(data=request.DATA)
#        if serializer.is_valid():
#            serializer.save()
#            return Response(serializer.data, status=status.HTTP_201_CREATED)
#        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#class SnippetList(mixins.ListModelMixin,
#                  mixins.CreateModelMixin,
#                  generics.GenericAPIView):
#    # `queryset` and `serializer_class` added by `GenericAPIView`.
#    queryset = Snippet.objects.all()
#    serializer_class = SnippetSerializer
#
#    def get(self, request, *args, **kwargs):
#        # `list` method provided by `mixins.ListModelMixin`.
#        return self.list(request, *args, **kwargs)
#
#    def post(self, request, *args, **kwargs):
#        # `create` method provided by `mixins.CreateModelMixin`.
#        return self.create(request, *args, **kwargs)

class SnippetList(generics.ListCreateAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def pre_save(self, obj):
        obj.owner = self.request.user




#class SnippetDetail(APIView):
#    """
#    Retrieve, update or delete a snippet instance.
#    """
#    def get_object(self, pk):
#        try:
#            return Snippet.objects.get(pk=pk)
#        except Snippet.DoesNotExist:
#            raise Http404
#
#    def get(self, request, pk, format=None):
#        snippet = self.get_object(pk)
#        serializer = SnippetSerializer(snippet)
#        return Response(serializer.data)
#
#    def put(self, request, pk, format=None):
#        snippet = self.get_object(pk)
#        serializer = SnippetSerializer(snippet, data=request.DATA)
#        if serializer.is_valid():
#            serializer.save()
#            return Response(serializer.data)
#        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#    def delete(self, request, pk, format=None):
#        snippet = self.get_object(pk)
#        snippet.delete()
#        return Response(status=status.HTTP_204_NO_CONTENT)

#class SnippetDetail(mixins.RetrieveModelMixin,
#                    mixins.UpdateModelMixin,
#                    mixins.DestroyModelMixin,
#                    generics.GenericAPIView):
#    # `queryset` and `serializer_class` added by `GenericAPIView`.
#    queryset = Snippet.objects.all()
#    serializer_class = SnippetSerializer
#
#    def get(self, request, *args, **kwargs):
#        # `retrieve` method provided by `mixins.RetrieveModelMixin`.
#        return self.retrieve(request, *args, **kwargs)
#
#    def put(self, request, *args, **kwargs):
#        # `update` method provided by `mixins.UpdateModelMixin`.
#        return self.update(request, *args, **kwargs)
#
#    def delete(self, request, *args, **kwargs):
#        # `destroy` method provided by mixins.DestroyModelMixin.
#        return self.destroy(request, *args, **kwargs)

class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)

    def pre_save(self, obj):
        obj.owner = self.request.user



class SnippetHighlight(generics.GenericAPIView):
    """
    In this case we want to return a property (`highlighted`) of an object instance (a `Snippet`
    instance), not an object instance itself. So there is no existing concrete generic view that
    we can use, we need to use the base class for representing instances.
    """
    queryset = Snippet.objects.all()
    # We use this specific renderer because we want to return the static HTML code which is stored
    # in the `highlighted` attribute of a `Snippet` instance.
    renderer_classes = (renderers.StaticHTMLRenderer,)

    def get(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)