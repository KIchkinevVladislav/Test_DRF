from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView

from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

from .views import (
    RegisterView,
    TokenView,
    UserViewSet,
    ImageView,
    ListOrDeleteImage,
    UserCurrentViewSet,
)

router = DefaultRouter()
router.register(r'current_user', UserCurrentViewSet, basename='current_user')
router.register(r'users', UserViewSet, basename='users')
image_router = routers.NestedSimpleRouter(router, r'users', lookup='users')
image_router.register(r'images', ImageView, basename='images')

urlpatterns = [
    path('v1/images_delete/', ListOrDeleteImage.as_view(), name='images_delete'),
    path('v1/', include(router.urls)),
    path('v1/', include(image_router.urls)),
    path('v1/auth/email/', RegisterView.as_view(), name='get_confirmation_code'),
    path('v1/auth/token/', TokenView.as_view(), name='get_token'),
    path('v1/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh')
]
