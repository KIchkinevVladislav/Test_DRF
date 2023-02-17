from django.shortcuts import get_object_or_404
from rest_framework import (
    viewsets,
    filters,
    generics,
    permissions,
    pagination,
    status
)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from django.core.mail import send_mail

from .models import User, Image
from .selializers import (
    RegisterSerializer,
    TokenSerializer,
    UserSerializer,
    ImageSerializer
)

from .permissions import IsAdminUser

class RegisterView(generics.CreateAPIView):
    """
    A cconfirmation_code is sent to the mail received from the user
    """
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.confirmation_code = serializer.validated_data[
                'confirmation_code'
            ]
            serializer.email = serializer.validated_data['email']
            serializer.save()
            send_mail(
                'Авторизация',
                f'confirmation_code = {serializer.confirmation_code} email = {serializer.email}',
                'admin@m.mi',
                [f'{serializer.email}'],
                fail_silently=False,
            )
        return Response(serializer.data)


class TokenView(APIView):
    """
    Sending the generated token to the user
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({'token': serializer.validated_data['token']})


class UserViewSet(viewsets.ModelViewSet):
    """
    Viewset for working with users
    Function get_or_update_self allows the user to change information about himself
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = pagination.PageNumberPagination
    permission_classes = [IsAdminUser, permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = [
        'name',
    ]
    lookup_field = 'username'

    @action(detail=False, permission_classes=(permissions.IsAuthenticated,), methods=['get', 'patch'], url_path='me')
    def get_or_update_self(self, request):
        if request.method != 'GET':
            serializer = self.get_serializer(
                instance=request.user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        else:
            serializer = self.get_serializer(request.user, many=False)
            return Response(serializer.data)


class ImageView(viewsets.ModelViewSet):
    """
    CRUD for Image
    """

    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = pagination.PageNumberPagination

    def get_image(self):
        image = get_object_or_404(Image, id=self.kwargs['image_pk'])
        return image

    def get_queryset(self):
        queryset = Image.objects.filter(image=self.get_image())
        return queryset

    def post(self, request, *args, **kwargs):
        print(request.data)
        file_serializer = ImageSerializer(data=request.data)
        print(file_serializer)
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(
                file_serializer.data,
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                file_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def put(self, request):
        imageid = self.request.POST.get('id')
        f_obj = Image.objects.filter(id=imageid)
        file_serializer = ImageSerializer(f_obj, data=request.data)
        print(file_serializer)
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(
                file_serializer.data,
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                file_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request):
        imageid = self.request.POST.get('id')
        f_obj = Image.objects.filter(id=imageid)
        if f_obj.exists():
            f_obj.delete()
            return Response(
                {
                    "Status": True,
                    "Message": "image deleted"
                }
            )


class ListOrDeleteImage(generics.GenericAPIView):
    """
    Administrator can delete all images from the database
    """
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [IsAdminUser]

    def delete(self, request):
        queryset = self.get_queryset()
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserCurrentViewSet(viewsets.ModelViewSet):
    """
    Return current user
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        pk = self.kwargs.get('pk')

        if pk == 'current':
            return self.request.user

        return super().get_object()
