from users.apps import UsersConfig
from django.urls import path
import users.views as v
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = UsersConfig.name

urlpatterns = [
    path('', v.UserListAPIView.as_view(), name='users_list'),
    path('create/', v.UserCreateAPIView.as_view(), name='user_create'),
    path('<int:pk>/', v.UserRetrieveAPIView.as_view(), name='user_get'),
    path('update/<int:pk>/', v.UserUpdateAPIView.as_view(), name='user_update'),
    path('delete/<int:pk>/', v.UserDestroyAPIView.as_view(), name='user_delete'),
    path('token/', TokenObtainPairView.as_view(), name='user_login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('sort_by_tasks/', v.UserWithTasksListAPIView.as_view(), name='sorted_user_list_by_tasks')
]
